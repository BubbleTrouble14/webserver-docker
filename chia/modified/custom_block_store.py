import logging
from typing import Dict, List, Optional, Tuple

import aiosqlite
import psycopg2

from chia.consensus.block_record import BlockRecord
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.blockchain_format.sub_epoch_summary import SubEpochSummary
from chia.types.full_block import FullBlock
from chia.types.weight_proof import SubEpochChallengeSegment, SubEpochSegments
from chia.util.custom_db_wrapper import DBWrapper
from chia.util.ints import uint32
from chia.util.lru_cache import LRUCache
from chia.util.bech32m import encode_puzzle_hash

log = logging.getLogger(__name__)


class BlockStore:
    db: aiosqlite.Connection
    block_cache: LRUCache
    db_wrapper: DBWrapper
    ses_challenge_cache: LRUCache

    @classmethod
    async def create(cls, db_wrapper: DBWrapper):
        self = cls()
        
        self.pgdb = db_wrapper.pgdb
        cursor_1 = self.pgdb.cursor()

        create_table_full_blocks_query = '''CREATE TABLE IF NOT EXISTS full_blocks
            (header_hash char(64) PRIMARY KEY,
                weight bigint,
                height integer,
                total_iters bigint,
                signage_point_index smallint,
                pos_ss_cc_challenge_hash char(64),
                proof_of_space_challenge char(64),
                proof_of_space_pool_public_key char(96),
                proof_of_space_pool_contract_puzzle_hash char(64),
                proof_of_space_plot_public_key char(96),
                proof_of_space_size smallint,
                proof_of_space_proof bytea,
                challenge_chain_sp_vdf_challenge char(64),
                challenge_chain_sp_vdf_number_of_iterations bigint,
                challenge_chain_sp_vdf_output_data char(200),
                challenge_chain_sp_signature char(192),
                challenge_chain_ip_vdf_challenge char(64),
                challenge_chain_ip_vdf_number_of_iterations bigint,
                challenge_chain_ip_vdf_output_data char(200),
                reward_chain_sp_vdf_challenge char(64),
                reward_chain_sp_vdf_number_of_iterations bigint,
                reward_chain_sp_vdf_output_data char(200),
                reward_chain_sp_signature char(192),
                reward_chain_ip_vdf_challenge char(64),
                reward_chain_ip_vdf_number_of_iterations bigint,
                reward_chain_ip_vdf_output_data char(200),
                infused_challenge_chain_ip_vdf_challenge char(64),
                infused_challenge_chain_ip_vdf_number_of_iterations bigint,
                infused_challenge_chain_ip_vdf_output_data char(200),
                is_tx_block boolean,
                challenge_chain_sp_proof_witness_type smallint,
                challenge_chain_sp_proof_witness bytea,
                challenge_chain_sp_proof_normalized_to_identity boolean,
                challenge_chain_ip_proof_witness_type smallint,
                challenge_chain_ip_proof_witness bytea,
                challenge_chain_ip_proof_normalized_to_identity boolean,
                reward_chain_sp_proof_witness_type smallint,
                reward_chain_sp_proof_witness bytea,
                reward_chain_sp_proof_normalized_to_identity boolean,
                reward_chain_ip_proof_witness_type smallint,
                reward_chain_ip_proof_witness bytea,
                reward_chain_ip_proof_normalized_to_identity boolean,         
                infused_challenge_chain_ip_proof_witness_type smallint,
                infused_challenge_chain_ip_proof_witness bytea,
                infused_challenge_chain_ip_proof_normalized_to_identity boolean,                    
                prev_header_hash char(64),
                reward_block_hash char(64),
                foliage_block_data_unfinished_reward_block_hash char(64),
                foliage_block_data_pool_target_puzzle_hash char(64),
                foliage_block_data_pool_target_address char(62),
                foliage_block_data_pool_target_max_height smallint,
                foliage_block_data_pool_signature char(192),
                foliage_block_data_farmer_reward_puzzle_hash char(64),
                foliage_block_data_farmer_reward_address char(62),
                foliage_block_data_extension_data char(64),
                foliage_block_data_signature char(192),
                foliage_transaction_block_hash char(64),
                foliage_transaction_block_signature char(192),          
                foliage_transaction_block_prev_transaction_block_hash char(64),
                foliage_transaction_block_timestamp bigint,
                foliage_transaction_block_filter_hash char(64),
                foliage_transaction_block_additions_root char(64),
                foliage_transaction_block_removals_root char(64),
                foliage_transaction_block_transactions_info_hash char(64),    
                transactions_info_generator_root char(64),
                transactions_info_generator_refs_root char(64),
                transactions_info_aggregated_signature char(192),
                transactions_info_fees bigint,
                transactions_info_cost bigint); '''
        # finished_sub_slots: List[EndOfSubSlotBundle]  # If first sb
        # transactions_info_reward_claims_incorporated List[Coin]  # These can be in any order
        # transactions_generator Optional[SerializedProgram]  # Program that generates transactions
        # transactions_generator_ref_list List[uint32]  # List of block heights of previous generators referenced in this block
        
        cursor_1.execute(create_table_full_blocks_query)
        self.pgdb.commit()
        cursor_1.close()

        cursor_2 = self.pgdb.cursor()
        create_table_reward_claims_incorporated_query = '''CREATE TABLE IF NOT EXISTS full_blocks_transactions_info_reward_claims_incorporated
            (header_hash char(64),
                parent_coin_info char(64),
                puzzle_hash char(64),
                address char(62),
                amount numeric(21, 0),
                PRIMARY KEY(header_hash, parent_coin_info)); '''

        cursor_2.execute(create_table_reward_claims_incorporated_query)
        self.pgdb.commit()
        cursor_2.close()

        # All full blocks which have been added to the blockchain. Header_hash -> block
        self.db_wrapper = db_wrapper
        self.db = db_wrapper.db
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS full_blocks(header_hash text PRIMARY KEY, height bigint,"
            "  is_block tinyint, is_fully_compactified tinyint, block blob)"
        )

        # Block records
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS block_records(header_hash "
            "text PRIMARY KEY, prev_hash text, height bigint,"
            "block blob, sub_epoch_summary blob, is_peak tinyint, is_block tinyint)"
        )

        # todo remove in v1.2
        await self.db.execute("DROP TABLE IF EXISTS sub_epoch_segments_v2")

        # Sub epoch segments for weight proofs
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS sub_epoch_segments_v3(ses_block_hash text PRIMARY KEY, challenge_segments blob)"
        )

        # Height index so we can look up in order of height for sync purposes
        await self.db.execute("CREATE INDEX IF NOT EXISTS full_block_height on full_blocks(height)")
        # this index is not used by any queries, don't create it for new
        # installs, and remove it from existing installs in the future
        # await self.db.execute("DROP INDEX IF EXISTS is_block on full_blocks(is_block)")
        await self.db.execute("CREATE INDEX IF NOT EXISTS is_fully_compactified on full_blocks(is_fully_compactified)")

        await self.db.execute("CREATE INDEX IF NOT EXISTS height on block_records(height)")

        await self.db.execute("CREATE INDEX IF NOT EXISTS hh on block_records(header_hash)")
        await self.db.execute("CREATE INDEX IF NOT EXISTS peak on block_records(is_peak)")

        # this index is not used by any queries, don't create it for new
        # installs, and remove it from existing installs in the future
        # await self.db.execute("DROP INDEX IF EXISTS is_block on block_records(is_block)")

        await self.db.commit()
        self.block_cache = LRUCache(1000)
        self.ses_challenge_cache = LRUCache(50)
        return self

    async def add_full_block(self, header_hash: bytes32, block: FullBlock, block_record: BlockRecord) -> None:
        self.block_cache.put(header_hash, block)

        pgdb_cursor = self.pgdb.cursor()
        pgdb_cursor.execute("INSERT INTO full_blocks (header_hash, weight, height, total_iters, signage_point_index, pos_ss_cc_challenge_hash, proof_of_space_challenge, proof_of_space_pool_public_key, proof_of_space_pool_contract_puzzle_hash, proof_of_space_plot_public_key, proof_of_space_size, proof_of_space_proof, challenge_chain_sp_vdf_challenge, challenge_chain_sp_vdf_number_of_iterations, challenge_chain_sp_vdf_output_data, challenge_chain_sp_signature, challenge_chain_ip_vdf_challenge, challenge_chain_ip_vdf_number_of_iterations, challenge_chain_ip_vdf_output_data, reward_chain_sp_vdf_challenge, reward_chain_sp_vdf_number_of_iterations, reward_chain_sp_vdf_output_data, reward_chain_sp_signature, reward_chain_ip_vdf_challenge, reward_chain_ip_vdf_number_of_iterations, reward_chain_ip_vdf_output_data, infused_challenge_chain_ip_vdf_challenge, infused_challenge_chain_ip_vdf_number_of_iterations, infused_challenge_chain_ip_vdf_output_data, is_tx_block, challenge_chain_sp_proof_witness_type, challenge_chain_sp_proof_witness, challenge_chain_sp_proof_normalized_to_identity, challenge_chain_ip_proof_witness_type, challenge_chain_ip_proof_witness, challenge_chain_ip_proof_normalized_to_identity, reward_chain_sp_proof_witness_type, reward_chain_sp_proof_witness, reward_chain_sp_proof_normalized_to_identity, reward_chain_ip_proof_witness_type, reward_chain_ip_proof_witness, reward_chain_ip_proof_normalized_to_identity, infused_challenge_chain_ip_proof_witness_type, infused_challenge_chain_ip_proof_witness, infused_challenge_chain_ip_proof_normalized_to_identity, prev_header_hash, reward_block_hash, foliage_block_data_unfinished_reward_block_hash, foliage_block_data_pool_target_puzzle_hash, foliage_block_data_pool_target_address, foliage_block_data_pool_target_max_height, foliage_block_data_pool_signature, foliage_block_data_farmer_reward_puzzle_hash, foliage_block_data_farmer_reward_address, foliage_block_data_extension_data, foliage_block_data_signature, foliage_transaction_block_hash, foliage_transaction_block_signature, foliage_transaction_block_prev_transaction_block_hash, foliage_transaction_block_timestamp, foliage_transaction_block_filter_hash, foliage_transaction_block_additions_root, foliage_transaction_block_removals_root, foliage_transaction_block_transactions_info_hash, transactions_info_generator_root, transactions_info_generator_refs_root, transactions_info_aggregated_signature, transactions_info_fees, transactions_info_cost) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        (
            header_hash.hex(),
            block.reward_chain_block.weight,
            block.reward_chain_block.height,
            block.reward_chain_block.total_iters,
            block.reward_chain_block.signage_point_index,
            block.reward_chain_block.pos_ss_cc_challenge_hash.hex(),
            block.reward_chain_block.proof_of_space.challenge.hex(),
            block.proof_of_space_pool_public_key(),
            block.proof_of_space_pool_contract_puzzle_hash(),
            bytes(block.reward_chain_block.proof_of_space.plot_public_key).hex(),
            block.reward_chain_block.proof_of_space.size,
            block.reward_chain_block.proof_of_space.proof,
            block.challenge_chain_sp_vdf_challange(),
            block.challenge_chain_sp_vdf_number_of_iterations(),
            block.challenge_chain_sp_vdf_challange_output_data(),
            bytes(block.reward_chain_block.challenge_chain_sp_signature).hex(),
            block.reward_chain_block.challenge_chain_ip_vdf.challenge.hex(),
            block.reward_chain_block.challenge_chain_ip_vdf.number_of_iterations,
            block.reward_chain_block.challenge_chain_ip_vdf.output.data.hex(),
            block.reward_chain_sp_vdf_challange(),
            block.reward_chain_sp_vdf_number_of_iterations(),
            block.reward_chain_sp_vdf_challange_output_data(),
            bytes(block.reward_chain_block.reward_chain_sp_signature).hex(),
            block.reward_chain_block.reward_chain_ip_vdf.challenge.hex(),
            block.reward_chain_block.reward_chain_ip_vdf.number_of_iterations,
            block.reward_chain_block.reward_chain_ip_vdf.output.data.hex(),
            block.infused_challenge_chain_ip_vdf_challange(),
            block.infused_challenge_chain_ip_vdf_number_of_iterations(),
            block.infused_challenge_chain_ip_vdf_challange_output_data(),
            block.is_transaction_block(),
            block.challenge_chain_sp_proof_witness_type(),
            block.challenge_chain_sp_proof_witness(),
            block.challenge_chain_sp_proof_normalized_to_identity(),
            block.challenge_chain_ip_proof.witness_type,
            block.challenge_chain_ip_proof.witness,
            block.challenge_chain_ip_proof.normalized_to_identity,
            block.reward_chain_sp_proof_witness_type(),
            block.reward_chain_sp_proof_witness(),
            block.reward_chain_sp_proof_normalized_to_identity(),
            block.reward_chain_ip_proof.witness_type,
            block.reward_chain_ip_proof.witness,
            block.reward_chain_ip_proof.normalized_to_identity,
            block.infused_challenge_chain_ip_proof_witness_type(),
            block.infused_challenge_chain_ip_proof_witness(),
            block.infused_challenge_chain_ip_proof_normalized_to_identity(),
            block.foliage.prev_block_hash.hex(),
            block.foliage.reward_block_hash.hex(),
            block.foliage.foliage_block_data.unfinished_reward_block_hash.hex(),
            block.foliage.foliage_block_data.pool_target.puzzle_hash.hex(),
            encode_puzzle_hash(block.foliage.foliage_block_data.pool_target.puzzle_hash, "xch"),
            block.foliage.foliage_block_data.pool_target.max_height,
            block.foliage_block_data_pool_signature(),
            block.foliage.foliage_block_data.farmer_reward_puzzle_hash.hex(),
            encode_puzzle_hash(block.foliage.foliage_block_data.farmer_reward_puzzle_hash, "xch"),
            block.foliage.foliage_block_data.extension_data.hex(),
            bytes(block.foliage.foliage_block_data_signature).hex(),
            block.foliage_transaction_block_hash(),
            block.foliage_transaction_block_signature(),
            block.foliage_transaction_block_prev_transaction_block_hash(),
            block.foliage_transaction_block_timestamp(),
            block.foliage_transaction_block_filter_hash(),
            block.foliage_transaction_block_additions_root(),
            block.foliage_transaction_block_removals_root(),
            block.foliage_transaction_block_transactions_info_hash(),  
            block.transactions_info_generator_root(),
            block.transactions_info_generator_refs_root(),
            block.transactions_info_aggregated_signature(),
            block.transactions_info_fees(),
            block.transactions_info_cost(),
        ))
        self.pgdb.commit()
        pgdb_cursor.close()


        if(block.is_transaction_block()):
            values = []
            for coin in block.reward_claims_incorporated():
                values.append(
                    (
                        header_hash.hex(),
                        coin.parent_coin_info.hex(),
                        coin.puzzle_hash.hex(),
                        encode_puzzle_hash(coin.puzzle_hash, "xch"),
                        coin.amount,
                    )
                )

            pgdb_cursor_1 = self.pgdb.cursor()
            pgdb_cursor_1.executemany(
                "INSERT INTO full_blocks_transactions_info_reward_claims_incorporated (header_hash, parent_coin_info, puzzle_hash, address, amount) VALUES(%s, %s, %s, %s, %s)", 
                values,
            )
            self.pgdb.commit()
            pgdb_cursor_1.close()


        cursor_1 = await self.db.execute(
            "INSERT OR REPLACE INTO full_blocks VALUES(?, ?, ?, ?, ?)",
            (
                header_hash.hex(),
                block.height,
                int(block.is_transaction_block()),
                int(block.is_fully_compactified()),
                bytes(block),
            ),
        )

        await cursor_1.close()

        cursor_2 = await self.db.execute(
            "INSERT OR REPLACE INTO block_records VALUES(?, ?, ?, ?,?, ?, ?)",
            (
                header_hash.hex(),
                block.prev_header_hash.hex(),
                block.height,
                bytes(block_record),
                None
                if block_record.sub_epoch_summary_included is None
                else bytes(block_record.sub_epoch_summary_included),
                False,
                block.is_transaction_block(),
            ),
        )
        await cursor_2.close()

    async def persist_sub_epoch_challenge_segments(
        self, ses_block_hash: bytes32, segments: List[SubEpochChallengeSegment]
    ) -> None:
        async with self.db_wrapper.lock:
            cursor_1 = await self.db.execute(
                "INSERT OR REPLACE INTO sub_epoch_segments_v3 VALUES(?, ?)",
                (ses_block_hash.hex(), bytes(SubEpochSegments(segments))),
            )
            await cursor_1.close()
            await self.db.commit()

    async def get_sub_epoch_challenge_segments(
        self,
        ses_block_hash: bytes32,
    ) -> Optional[List[SubEpochChallengeSegment]]:
        cached = self.ses_challenge_cache.get(ses_block_hash)
        if cached is not None:
            return cached
        cursor = await self.db.execute(
            "SELECT challenge_segments from sub_epoch_segments_v3 WHERE ses_block_hash=?", (ses_block_hash.hex(),)
        )
        row = await cursor.fetchone()
        await cursor.close()
        if row is not None:
            challenge_segments = SubEpochSegments.from_bytes(row[0]).challenge_segments
            self.ses_challenge_cache.put(ses_block_hash, challenge_segments)
            return challenge_segments
        return None

    def rollback_cache_block(self, header_hash: bytes32):
        try:
            self.block_cache.remove(header_hash)
        except KeyError:
            # this is best effort. When rolling back, we may not have added the
            # block to the cache yet
            pass

    async def get_full_block(self, header_hash: bytes32) -> Optional[FullBlock]:
        cached = self.block_cache.get(header_hash)
        if cached is not None:
            log.debug(f"cache hit for block {header_hash.hex()}")
            return cached
        log.debug(f"cache miss for block {header_hash.hex()}")
        cursor = await self.db.execute("SELECT block from full_blocks WHERE header_hash=?", (header_hash.hex(),))
        row = await cursor.fetchone()
        await cursor.close()
        if row is not None:
            block = FullBlock.from_bytes(row[0])
            self.block_cache.put(header_hash, block)
            return block
        return None

    async def get_full_block_bytes(self, header_hash: bytes32) -> Optional[bytes]:
        cached = self.block_cache.get(header_hash)
        if cached is not None:
            log.debug(f"cache hit for block {header_hash.hex()}")
            return bytes(cached)
        log.debug(f"cache miss for block {header_hash.hex()}")
        cursor = await self.db.execute("SELECT block from full_blocks WHERE header_hash=?", (header_hash.hex(),))
        row = await cursor.fetchone()
        await cursor.close()
        if row is not None:
            return row[0]
        return None

    async def get_full_blocks_at(self, heights: List[uint32]) -> List[FullBlock]:
        if len(heights) == 0:
            return []

        heights_db = tuple(heights)
        formatted_str = f'SELECT block from full_blocks WHERE height in ({"?," * (len(heights_db) - 1)}?)'
        cursor = await self.db.execute(formatted_str, heights_db)
        rows = await cursor.fetchall()
        await cursor.close()
        return [FullBlock.from_bytes(row[0]) for row in rows]

    async def get_block_records_by_hash(self, header_hashes: List[bytes32]):
        """
        Returns a list of Block Records, ordered by the same order in which header_hashes are passed in.
        Throws an exception if the blocks are not present
        """
        if len(header_hashes) == 0:
            return []

        header_hashes_db = tuple([hh.hex() for hh in header_hashes])
        formatted_str = f'SELECT block from block_records WHERE header_hash in ({"?," * (len(header_hashes_db) - 1)}?)'
        cursor = await self.db.execute(formatted_str, header_hashes_db)
        rows = await cursor.fetchall()
        await cursor.close()
        all_blocks: Dict[bytes32, BlockRecord] = {}
        for row in rows:
            block_rec: BlockRecord = BlockRecord.from_bytes(row[0])
            all_blocks[block_rec.header_hash] = block_rec
        ret: List[BlockRecord] = []
        for hh in header_hashes:
            if hh not in all_blocks:
                raise ValueError(f"Header hash {hh} not in the blockchain")
            ret.append(all_blocks[hh])
        return ret

    async def get_blocks_by_hash(self, header_hashes: List[bytes32]) -> List[FullBlock]:
        """
        Returns a list of Full Blocks blocks, ordered by the same order in which header_hashes are passed in.
        Throws an exception if the blocks are not present
        """

        if len(header_hashes) == 0:
            return []

        header_hashes_db = tuple([hh.hex() for hh in header_hashes])
        formatted_str = (
            f'SELECT header_hash, block from full_blocks WHERE header_hash in ({"?," * (len(header_hashes_db) - 1)}?)'
        )
        cursor = await self.db.execute(formatted_str, header_hashes_db)
        rows = await cursor.fetchall()
        await cursor.close()
        all_blocks: Dict[bytes32, FullBlock] = {}
        for row in rows:
            header_hash = bytes.fromhex(row[0])
            full_block: FullBlock = FullBlock.from_bytes(row[1])
            all_blocks[header_hash] = full_block
            self.block_cache.put(header_hash, full_block)
        ret: List[FullBlock] = []
        for hh in header_hashes:
            if hh not in all_blocks:
                raise ValueError(f"Header hash {hh} not in the blockchain")
            ret.append(all_blocks[hh])
        return ret

    async def get_block_record(self, header_hash: bytes32) -> Optional[BlockRecord]:
        cursor = await self.db.execute(
            "SELECT block from block_records WHERE header_hash=?",
            (header_hash.hex(),),
        )
        row = await cursor.fetchone()
        await cursor.close()
        if row is not None:
            return BlockRecord.from_bytes(row[0])
        return None

    async def get_block_records_in_range(
        self,
        start: int,
        stop: int,
    ) -> Dict[bytes32, BlockRecord]:
        """
        Returns a dictionary with all blocks in range between start and stop
        if present.
        """

        formatted_str = f"SELECT header_hash, block from block_records WHERE height >= {start} and height <= {stop}"

        cursor = await self.db.execute(formatted_str)
        rows = await cursor.fetchall()
        await cursor.close()
        ret: Dict[bytes32, BlockRecord] = {}
        for row in rows:
            header_hash = bytes.fromhex(row[0])
            ret[header_hash] = BlockRecord.from_bytes(row[1])

        return ret

    async def get_block_records_close_to_peak(
        self, blocks_n: int
    ) -> Tuple[Dict[bytes32, BlockRecord], Optional[bytes32]]:
        """
        Returns a dictionary with all blocks that have height >= peak height - blocks_n, as well as the
        peak header hash.
        """

        res = await self.db.execute("SELECT * from block_records WHERE is_peak = 1")
        peak_row = await res.fetchone()
        await res.close()
        if peak_row is None:
            return {}, None

        formatted_str = f"SELECT header_hash, block  from block_records WHERE height >= {peak_row[2] - blocks_n}"
        cursor = await self.db.execute(formatted_str)
        rows = await cursor.fetchall()
        await cursor.close()
        ret: Dict[bytes32, BlockRecord] = {}
        for row in rows:
            header_hash = bytes.fromhex(row[0])
            ret[header_hash] = BlockRecord.from_bytes(row[1])
        return ret, bytes.fromhex(peak_row[0])

    async def get_peak_height_dicts(self) -> Tuple[Dict[uint32, bytes32], Dict[uint32, SubEpochSummary]]:
        """
        Returns a dictionary with all blocks, as well as the header hash of the peak,
        if present.
        """

        res = await self.db.execute("SELECT * from block_records WHERE is_peak = 1")
        row = await res.fetchone()
        await res.close()
        if row is None:
            return {}, {}

        peak: bytes32 = bytes.fromhex(row[0])
        cursor = await self.db.execute("SELECT header_hash,prev_hash,height,sub_epoch_summary from block_records")
        rows = await cursor.fetchall()
        await cursor.close()
        hash_to_prev_hash: Dict[bytes32, bytes32] = {}
        hash_to_height: Dict[bytes32, uint32] = {}
        hash_to_summary: Dict[bytes32, SubEpochSummary] = {}

        for row in rows:
            hash_to_prev_hash[bytes.fromhex(row[0])] = bytes.fromhex(row[1])
            hash_to_height[bytes.fromhex(row[0])] = row[2]
            if row[3] is not None:
                hash_to_summary[bytes.fromhex(row[0])] = SubEpochSummary.from_bytes(row[3])

        height_to_hash: Dict[uint32, bytes32] = {}
        sub_epoch_summaries: Dict[uint32, SubEpochSummary] = {}

        curr_header_hash = peak
        curr_height = hash_to_height[curr_header_hash]
        while True:
            height_to_hash[curr_height] = curr_header_hash
            if curr_header_hash in hash_to_summary:
                sub_epoch_summaries[curr_height] = hash_to_summary[curr_header_hash]
            if curr_height == 0:
                break
            curr_header_hash = hash_to_prev_hash[curr_header_hash]
            curr_height = hash_to_height[curr_header_hash]
        return height_to_hash, sub_epoch_summaries

    async def set_peak(self, header_hash: bytes32) -> None:
        # We need to be in a sqlite transaction here.
        # Note: we do not commit this to the database yet, as we need to also change the coin store
        cursor_1 = await self.db.execute("UPDATE block_records SET is_peak=0 WHERE is_peak=1")
        await cursor_1.close()
        cursor_2 = await self.db.execute(
            "UPDATE block_records SET is_peak=1 WHERE header_hash=?",
            (header_hash.hex(),),
        )
        await cursor_2.close()

    async def is_fully_compactified(self, header_hash: bytes32) -> Optional[bool]:
        cursor = await self.db.execute(
            "SELECT is_fully_compactified from full_blocks WHERE header_hash=?", (header_hash.hex(),)
        )
        row = await cursor.fetchone()
        await cursor.close()
        if row is None:
            return None
        return bool(row[0])

    async def get_random_not_compactified(self, number: int) -> List[int]:
        # Since orphan blocks do not get compactified, we need to check whether all blocks with a
        # certain height are not compact. And if we do have compact orphan blocks, then all that
        # happens is that the occasional chain block stays uncompact - not ideal, but harmless.
        cursor = await self.db.execute(
            f"SELECT height FROM full_blocks GROUP BY height HAVING sum(is_fully_compactified)=0 "
            f"ORDER BY RANDOM() LIMIT {number}"
        )
        rows = await cursor.fetchall()
        await cursor.close()

        heights = []
        for row in rows:
            heights.append(int(row[0]))

        return heights