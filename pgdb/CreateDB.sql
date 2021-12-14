CREATE TABLE IF NOT EXISTS public.full_blocks
(
    header_hash character(64) COLLATE pg_catalog."default" NOT NULL,
    weight bigint,
    height integer,
    total_iters bigint,
    signage_point_index smallint,
    pos_ss_cc_challenge_hash character(64) COLLATE pg_catalog."default",
    proof_of_space_challenge character(64) COLLATE pg_catalog."default",
    proof_of_space_pool_public_key character(96) COLLATE pg_catalog."default",
    proof_of_space_pool_contract_puzzle_hash character(64) COLLATE pg_catalog."default",
    proof_of_space_plot_public_key character(96) COLLATE pg_catalog."default",
    proof_of_space_size smallint,
    proof_of_space_proof bytea,
    challenge_chain_sp_vdf_challenge character(64) COLLATE pg_catalog."default",
    challenge_chain_sp_vdf_number_of_iterations bigint,
    challenge_chain_sp_vdf_output_data character(200) COLLATE pg_catalog."default",
    challenge_chain_sp_signature character(192) COLLATE pg_catalog."default",
    challenge_chain_ip_vdf_challenge character(64) COLLATE pg_catalog."default",
    challenge_chain_ip_vdf_number_of_iterations bigint,
    challenge_chain_ip_vdf_output_data character(200) COLLATE pg_catalog."default",
    reward_chain_sp_vdf_challenge character(64) COLLATE pg_catalog."default",
    reward_chain_sp_vdf_number_of_iterations bigint,
    reward_chain_sp_vdf_output_data character(200) COLLATE pg_catalog."default",
    reward_chain_sp_signature character(192) COLLATE pg_catalog."default",
    reward_chain_ip_vdf_challenge character(64) COLLATE pg_catalog."default",
    reward_chain_ip_vdf_number_of_iterations bigint,
    reward_chain_ip_vdf_output_data character(200) COLLATE pg_catalog."default",
    infused_challenge_chain_ip_vdf_challenge character(64) COLLATE pg_catalog."default",
    infused_challenge_chain_ip_vdf_number_of_iterations bigint,
    infused_challenge_chain_ip_vdf_output_data character(200) COLLATE pg_catalog."default",
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
    prev_header_hash character(64) COLLATE pg_catalog."default",
    reward_block_hash character(64) COLLATE pg_catalog."default",
    foliage_block_data_unfinished_reward_block_hash character(64) COLLATE pg_catalog."default",
    foliage_block_data_pool_target_puzzle_hash character(64) COLLATE pg_catalog."default",
    foliage_block_data_pool_target_address character(62) COLLATE pg_catalog."default",
    foliage_block_data_pool_target_max_height smallint,
    foliage_block_data_pool_signature character(192) COLLATE pg_catalog."default",
    foliage_block_data_farmer_reward_puzzle_hash character(64) COLLATE pg_catalog."default",
    foliage_block_data_farmer_reward_address character(62) COLLATE pg_catalog."default",
    foliage_block_data_extension_data character(64) COLLATE pg_catalog."default",
    foliage_block_data_signature character(192) COLLATE pg_catalog."default",
    foliage_transaction_block_hash character(64) COLLATE pg_catalog."default",
    foliage_transaction_block_signature character(192) COLLATE pg_catalog."default",
    foliage_transaction_block_prev_transaction_block_hash character(64) COLLATE pg_catalog."default",
    foliage_transaction_block_timestamp bigint,
    foliage_transaction_block_filter_hash character(64) COLLATE pg_catalog."default",
    foliage_transaction_block_additions_root character(64) COLLATE pg_catalog."default",
    foliage_transaction_block_removals_root character(64) COLLATE pg_catalog."default",
    foliage_transaction_block_transactions_info_hash character(64) COLLATE pg_catalog."default",
    transactions_info_generator_root character(64) COLLATE pg_catalog."default",
    transactions_info_generator_refs_root character(64) COLLATE pg_catalog."default",
    transactions_info_aggregated_signature character(192) COLLATE pg_catalog."default",
    transactions_info_fees bigint,
    transactions_info_cost bigint,
    dollar_price numeric(12, 4),
    CONSTRAINT full_blocks_pkey PRIMARY KEY (header_hash)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.full_blocks
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS public.full_blocks_transactions_info_reward_claims_incorporated
(
    header_hash character(64) COLLATE pg_catalog."default" NOT NULL,
    parent_coin_info character(64) COLLATE pg_catalog."default" NOT NULL,
    puzzle_hash character(64) COLLATE pg_catalog."default",
    address character(62) COLLATE pg_catalog."default",
    amount numeric(21,0),
    CONSTRAINT full_blocks_transactions_info_reward_claims_incorporated_pkey PRIMARY KEY (header_hash, parent_coin_info)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.full_blocks_transactions_info_reward_claims_incorporated
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS public.coin_record
(
    coin_name character(64) COLLATE pg_catalog."default" NOT NULL,
    confirmed_index bigint,
    spent_index bigint,
    spent integer,
    coinbase integer,
    puzzle_hash character(64) COLLATE pg_catalog."default",
    address character(62) COLLATE pg_catalog."default",
    coin_parent character(64) COLLATE pg_catalog."default",
    amount numeric(21,0),
    "timestamp" bigint,
    CONSTRAINT coin_record_pkey PRIMARY KEY (coin_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.coin_record
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS public.logmessages
(
    msg text
);

ALTER TABLE IF EXISTS public.logmessages OWNER to postgres;

CREATE OR REPLACE PROCEDURE public.logmessage(IN msg1 text)

LANGUAGE 'plpgsql'
AS $BODY$

begin
INSERT INTO public.logmessages (
    msg
	)
VALUES(
    msg1
	);

end;
$BODY$;

GRANT EXECUTE ON ROUTINE public.logmessage(text) TO postgres;

-- call public.logmessage('ape');
-- select * from public.logmessages

CREATE OR REPLACE PROCEDURE public.save_full_block(
	IN headerHash character,
	IN weight bigint,
	IN height integer,
 	IN total_iters bigint,
 	IN signage_point_index integer,
	IN pos_ss_cc_challenge_hash character,
	IN proof_of_space_challenge character,
	IN proof_of_space_pool_public_key character,
	IN proof_of_space_pool_contract_puzzle_hash character,
	IN proof_of_space_plot_public_key character,
	IN proof_of_space_size integer,
	IN proof_of_space_proof bytea,
	IN challenge_chain_sp_vdf_challenge character,
	IN challenge_chain_sp_vdf_number_of_iterations bigint,
	IN challenge_chain_sp_vdf_output_data character,
	IN challenge_chain_sp_signature character,
	IN challenge_chain_ip_vdf_challenge character,
	IN challenge_chain_ip_vdf_number_of_iterations bigint,
	IN challenge_chain_ip_vdf_output_data character,
	IN reward_chain_sp_vdf_challenge character,
	IN reward_chain_sp_vdf_number_of_iterations bigint,
	IN reward_chain_sp_vdf_output_data character,
	IN reward_chain_sp_signature character,
	IN reward_chain_ip_vdf_challenge character,
	IN reward_chain_ip_vdf_number_of_iterations bigint,
	IN reward_chain_ip_vdf_output_data character,
	IN infused_challenge_chain_ip_vdf_challenge character,
	IN infused_challenge_chain_ip_vdf_number_of_iterations bigint,
	IN infused_challenge_chain_ip_vdf_output_data character,
	IN is_tx_block boolean,
	IN challenge_chain_sp_proof_witness_type integer,
	IN challenge_chain_sp_proof_witness bytea,
	IN challenge_chain_sp_proof_normalized_to_identity boolean,
	IN challenge_chain_ip_proof_witness_type integer,
	IN challenge_chain_ip_proof_witness bytea,
	IN challenge_chain_ip_proof_normalized_to_identity boolean,
	IN reward_chain_sp_proof_witness_type integer,
	IN reward_chain_sp_proof_witness bytea,
	IN reward_chain_sp_proof_normalized_to_identity boolean,
	IN reward_chain_ip_proof_witness_type integer,
	IN reward_chain_ip_proof_witness bytea,
	IN reward_chain_ip_proof_normalized_to_identity boolean,
	IN infused_challenge_chain_ip_proof_witness_type integer,
	IN infused_challenge_chain_ip_proof_witness bytea,
	IN infused_challenge_chain_ip_proof_normalized_to_identity boolean,
	IN prev_header_hash character,
	IN reward_block_hash character,
	IN foliage_block_data_unfinished_reward_block_hash character,
	IN foliage_block_data_pool_target_puzzle_hash character,
	IN foliage_block_data_pool_target_address character,
	IN foliage_block_data_pool_target_max_height integer,
	IN foliage_block_data_pool_signature character,
	IN foliage_block_data_farmer_reward_puzzle_hash character,
	IN foliage_block_data_farmer_reward_address character,
	IN foliage_block_data_extension_data character,
	IN foliage_block_data_signature character,
	IN foliage_transaction_block_hash character,
	IN foliage_transaction_block_signature character,
	IN foliage_transaction_block_prev_transaction_block_hash character,
	IN foliage_transaction_block_timestamp bigint,
	IN foliage_transaction_block_filter_hash character,
	IN foliage_transaction_block_additions_root character,
	IN foliage_transaction_block_removals_root character,
	IN foliage_transaction_block_transactions_info_hash character,
	IN transactions_info_generator_root character,
	IN transactions_info_generator_refs_root character,
	IN transactions_info_aggregated_signature character,
	IN transactions_info_fees bigint,
	IN transactions_info_cost bigint
)
LANGUAGE 'plpgsql'
AS $BODY$

begin

INSERT INTO public.full_blocks (
    header_hash,
    weight,
    height,
    total_iters,
    signage_point_index,
    pos_ss_cc_challenge_hash,
    proof_of_space_challenge,
    proof_of_space_pool_public_key,
    proof_of_space_pool_contract_puzzle_hash,
    proof_of_space_plot_public_key,
    proof_of_space_size,
    proof_of_space_proof,
    challenge_chain_sp_vdf_challenge,
    challenge_chain_sp_vdf_number_of_iterations,
    challenge_chain_sp_vdf_output_data,
    challenge_chain_sp_signature,
    challenge_chain_ip_vdf_challenge,
    challenge_chain_ip_vdf_number_of_iterations,
    challenge_chain_ip_vdf_output_data,
    reward_chain_sp_vdf_challenge,
    reward_chain_sp_vdf_number_of_iterations,
    reward_chain_sp_vdf_output_data,
    reward_chain_sp_signature,
    reward_chain_ip_vdf_challenge,
    reward_chain_ip_vdf_number_of_iterations,
    reward_chain_ip_vdf_output_data,
    infused_challenge_chain_ip_vdf_challenge,
    infused_challenge_chain_ip_vdf_number_of_iterations,
    infused_challenge_chain_ip_vdf_output_data,
    is_tx_block,
    challenge_chain_sp_proof_witness_type,
    challenge_chain_sp_proof_witness,
    challenge_chain_sp_proof_normalized_to_identity,
    challenge_chain_ip_proof_witness_type,
    challenge_chain_ip_proof_witness,
    challenge_chain_ip_proof_normalized_to_identity,
    reward_chain_sp_proof_witness_type,
    reward_chain_sp_proof_witness,
    reward_chain_sp_proof_normalized_to_identity,
    reward_chain_ip_proof_witness_type,
    reward_chain_ip_proof_witness,
    reward_chain_ip_proof_normalized_to_identity,         
    infused_challenge_chain_ip_proof_witness_type,
    infused_challenge_chain_ip_proof_witness,
    infused_challenge_chain_ip_proof_normalized_to_identity,                    
    prev_header_hash,
    reward_block_hash,
    foliage_block_data_unfinished_reward_block_hash,
    foliage_block_data_pool_target_puzzle_hash,
    foliage_block_data_pool_target_address,
    foliage_block_data_pool_target_max_height,
    foliage_block_data_pool_signature,
    foliage_block_data_farmer_reward_puzzle_hash,
    foliage_block_data_farmer_reward_address,
    foliage_block_data_extension_data,
    foliage_block_data_signature,
    foliage_transaction_block_hash,
    foliage_transaction_block_signature,
    foliage_transaction_block_prev_transaction_block_hash,
    foliage_transaction_block_timestamp,
    foliage_transaction_block_filter_hash,
    foliage_transaction_block_additions_root,
    foliage_transaction_block_removals_root,
    foliage_transaction_block_transactions_info_hash,
    transactions_info_generator_root,
    transactions_info_generator_refs_root,
    transactions_info_aggregated_signature,
    transactions_info_fees,
    transactions_info_cost
	)
VALUES(
    headerHash,
    weight,
    height,
    total_iters,
    signage_point_index,
    pos_ss_cc_challenge_hash,
    proof_of_space_challenge,
    proof_of_space_pool_public_key,
    proof_of_space_pool_contract_puzzle_hash,
    proof_of_space_plot_public_key,
    proof_of_space_size,
    proof_of_space_proof,
    challenge_chain_sp_vdf_challenge,
    challenge_chain_sp_vdf_number_of_iterations,
    challenge_chain_sp_vdf_output_data,
    challenge_chain_sp_signature,
    challenge_chain_ip_vdf_challenge,
    challenge_chain_ip_vdf_number_of_iterations,
    challenge_chain_ip_vdf_output_data,
    reward_chain_sp_vdf_challenge,
    reward_chain_sp_vdf_number_of_iterations,
    reward_chain_sp_vdf_output_data,
    reward_chain_sp_signature,
    reward_chain_ip_vdf_challenge,
    reward_chain_ip_vdf_number_of_iterations,
    reward_chain_ip_vdf_output_data,
    infused_challenge_chain_ip_vdf_challenge,
    infused_challenge_chain_ip_vdf_number_of_iterations,
    infused_challenge_chain_ip_vdf_output_data,
    is_tx_block,
    challenge_chain_sp_proof_witness_type,
    challenge_chain_sp_proof_witness,
    challenge_chain_sp_proof_normalized_to_identity,
    challenge_chain_ip_proof_witness_type,
    challenge_chain_ip_proof_witness,
    challenge_chain_ip_proof_normalized_to_identity,
    reward_chain_sp_proof_witness_type,
    reward_chain_sp_proof_witness,
    reward_chain_sp_proof_normalized_to_identity,
    reward_chain_ip_proof_witness_type,
    reward_chain_ip_proof_witness,
    reward_chain_ip_proof_normalized_to_identity,         
    infused_challenge_chain_ip_proof_witness_type,
    infused_challenge_chain_ip_proof_witness,
    infused_challenge_chain_ip_proof_normalized_to_identity,                    
    prev_header_hash,
    reward_block_hash,
    foliage_block_data_unfinished_reward_block_hash,
    foliage_block_data_pool_target_puzzle_hash,
    foliage_block_data_pool_target_address,
    foliage_block_data_pool_target_max_height,
    foliage_block_data_pool_signature,
    foliage_block_data_farmer_reward_puzzle_hash,
    foliage_block_data_farmer_reward_address,
    foliage_block_data_extension_data,
    foliage_block_data_signature,
    foliage_transaction_block_hash,
    foliage_transaction_block_signature,
    foliage_transaction_block_prev_transaction_block_hash,
    foliage_transaction_block_timestamp,
    foliage_transaction_block_filter_hash,
    foliage_transaction_block_additions_root,
    foliage_transaction_block_removals_root,
    foliage_transaction_block_transactions_info_hash,
    transactions_info_generator_root,
    transactions_info_generator_refs_root,
    transactions_info_aggregated_signature,
    transactions_info_fees,
    transactions_info_cost
	)
ON CONFLICT (header_hash) 
DO UPDATE SET 
   "weight" = EXCLUDED.weight,
    height = EXCLUDED.height,
    total_iters = EXCLUDED.total_iters,
    signage_point_index = EXCLUDED.signage_point_index,
    pos_ss_cc_challenge_hash = EXCLUDED.pos_ss_cc_challenge_hash,
    proof_of_space_challenge = EXCLUDED.proof_of_space_challenge,
    proof_of_space_pool_public_key = EXCLUDED.proof_of_space_challenge,
    proof_of_space_pool_contract_puzzle_hash = EXCLUDED.proof_of_space_challenge,
    proof_of_space_plot_public_key = EXCLUDED.proof_of_space_challenge,
    proof_of_space_size = EXCLUDED.proof_of_space_size,
    proof_of_space_proof = EXCLUDED.proof_of_space_proof,
    challenge_chain_sp_vdf_challenge = EXCLUDED.challenge_chain_sp_vdf_challenge,
    challenge_chain_sp_vdf_number_of_iterations = EXCLUDED.challenge_chain_sp_vdf_number_of_iterations,
    challenge_chain_sp_vdf_output_data = EXCLUDED.challenge_chain_sp_vdf_output_data,
    challenge_chain_sp_signature = EXCLUDED.challenge_chain_sp_signature,
    challenge_chain_ip_vdf_challenge = EXCLUDED.challenge_chain_ip_vdf_challenge,
    challenge_chain_ip_vdf_number_of_iterations = EXCLUDED.challenge_chain_ip_vdf_number_of_iterations,
    challenge_chain_ip_vdf_output_data = EXCLUDED.challenge_chain_ip_vdf_output_data,
    reward_chain_sp_vdf_challenge = EXCLUDED.reward_chain_sp_vdf_challenge,
    reward_chain_sp_vdf_number_of_iterations = EXCLUDED.reward_chain_sp_vdf_number_of_iterations,
    reward_chain_sp_vdf_output_data = EXCLUDED.reward_chain_sp_vdf_output_data,
    reward_chain_sp_signature = EXCLUDED.reward_chain_sp_signature,
    reward_chain_ip_vdf_challenge = EXCLUDED.reward_chain_ip_vdf_challenge,
    reward_chain_ip_vdf_number_of_iterations = EXCLUDED.reward_chain_ip_vdf_number_of_iterations,
    reward_chain_ip_vdf_output_data = EXCLUDED.reward_chain_ip_vdf_output_data,
    infused_challenge_chain_ip_vdf_challenge = EXCLUDED.infused_challenge_chain_ip_vdf_challenge,
    infused_challenge_chain_ip_vdf_number_of_iterations = EXCLUDED.infused_challenge_chain_ip_vdf_number_of_iterations,
    infused_challenge_chain_ip_vdf_output_data = EXCLUDED.infused_challenge_chain_ip_vdf_output_data,
    is_tx_block = EXCLUDED.is_tx_block,
    challenge_chain_sp_proof_witness_type = EXCLUDED.challenge_chain_sp_proof_witness_type,
    challenge_chain_sp_proof_witness = EXCLUDED.challenge_chain_sp_proof_witness,
    challenge_chain_sp_proof_normalized_to_identity = EXCLUDED.challenge_chain_sp_proof_normalized_to_identity,
    challenge_chain_ip_proof_witness_type = EXCLUDED.challenge_chain_ip_proof_witness_type,
    challenge_chain_ip_proof_witness = EXCLUDED.challenge_chain_ip_proof_witness,
    challenge_chain_ip_proof_normalized_to_identity = EXCLUDED.challenge_chain_ip_proof_normalized_to_identity,
    reward_chain_sp_proof_witness_type = EXCLUDED.reward_chain_sp_proof_witness_type,
    reward_chain_sp_proof_witness = EXCLUDED.reward_chain_sp_proof_witness,
    reward_chain_sp_proof_normalized_to_identity = EXCLUDED.reward_chain_sp_proof_normalized_to_identity,
    reward_chain_ip_proof_witness_type = EXCLUDED.reward_chain_ip_proof_witness_type,
    reward_chain_ip_proof_witness = EXCLUDED.reward_chain_ip_proof_witness,
    reward_chain_ip_proof_normalized_to_identity = EXCLUDED.reward_chain_ip_proof_normalized_to_identity,         
    infused_challenge_chain_ip_proof_witness_type = EXCLUDED.infused_challenge_chain_ip_proof_witness_type,
    infused_challenge_chain_ip_proof_witness = EXCLUDED.infused_challenge_chain_ip_proof_witness,
    infused_challenge_chain_ip_proof_normalized_to_identity = EXCLUDED.infused_challenge_chain_ip_proof_normalized_to_identity,                    
    prev_header_hash = EXCLUDED.prev_header_hash,
    reward_block_hash = EXCLUDED.reward_block_hash,
    foliage_block_data_unfinished_reward_block_hash = EXCLUDED.foliage_block_data_unfinished_reward_block_hash,
    foliage_block_data_pool_target_puzzle_hash = EXCLUDED.foliage_block_data_pool_target_puzzle_hash,
    foliage_block_data_pool_target_address = EXCLUDED.foliage_block_data_pool_target_address,
    foliage_block_data_pool_target_max_height = EXCLUDED.foliage_block_data_pool_target_max_height,
    foliage_block_data_pool_signature = EXCLUDED.foliage_block_data_pool_signature,
    foliage_block_data_farmer_reward_puzzle_hash = EXCLUDED.foliage_block_data_farmer_reward_puzzle_hash,
    foliage_block_data_farmer_reward_address = EXCLUDED.foliage_block_data_farmer_reward_address,
    foliage_block_data_extension_data = EXCLUDED.foliage_block_data_extension_data,
    foliage_block_data_signature = EXCLUDED.foliage_block_data_signature,
    foliage_transaction_block_hash = EXCLUDED.foliage_transaction_block_hash,
    foliage_transaction_block_signature = EXCLUDED.foliage_transaction_block_signature,
    foliage_transaction_block_prev_transaction_block_hash = EXCLUDED.foliage_transaction_block_prev_transaction_block_hash,
    foliage_transaction_block_timestamp = EXCLUDED.foliage_transaction_block_timestamp,
    foliage_transaction_block_filter_hash = EXCLUDED.foliage_transaction_block_filter_hash,
    foliage_transaction_block_additions_root = EXCLUDED.foliage_transaction_block_additions_root,
    foliage_transaction_block_removals_root = EXCLUDED.foliage_transaction_block_removals_root,
    foliage_transaction_block_transactions_info_hash = EXCLUDED.foliage_transaction_block_transactions_info_hash,
    transactions_info_generator_root = EXCLUDED.transactions_info_generator_root,
    transactions_info_generator_refs_root = EXCLUDED.transactions_info_generator_refs_root,
    transactions_info_aggregated_signature = EXCLUDED.transactions_info_aggregated_signature,
    transactions_info_fees = EXCLUDED.transactions_info_fees,
    transactions_info_cost = EXCLUDED.transactions_info_cost;
end;
$BODY$;


GRANT EXECUTE ON ROUTINE public.save_full_block(
	 character,
	 bigint,
	 integer,
	 bigint,
	 int,
	 character,
	 character,
	 character,
	 character,
	 character,
	 int,
	 bytea,
	 character,
	 bigint,
	 character,
	 character,
	 character,
	 bigint,
	 character,
	 character,
	 bigint,
	 character,
	 character,
	 character,
	 bigint,
	 character,
	 character,
	 bigint,
	 character,
	 boolean,
	 int,
	 bytea,
	 boolean,
	 int,
	 bytea,
	 boolean,
	 int,
	 bytea,
	 boolean,
	 int,
	 bytea,
	 boolean,
	 int,
	 bytea,
	 boolean,
	 character,
	 character,
	 character,
	 character,
	 character,
	 int,
	 character,
	 character,
	 character,
	 character,
	 character,
	 character,
	 character,
	 character,
	 bigint,
	 character,
	 character,
	 character,
	 character,
	 character,
	 character,
	 character,
	 bigint,
	 bigint
    ) TO postgres;


CREATE OR REPLACE PROCEDURE public.save_coin_record(
	IN coinName character,
	IN confirmed_index bigint,
	IN spent_index bigint,
	IN spent integer,
	IN coinbase integer,
	IN puzzle_hash character,
	IN address character,
	IN coin_parent character,
	IN amount numeric,
	IN time_stamp bigint)
LANGUAGE 'plpgsql'
AS $BODY$

begin

INSERT INTO public.coin_record (
    coin_name,
    confirmed_index,
    spent_index,
    spent,
    coinbase,
    puzzle_hash,
    address,
    coin_parent,
    amount,
    timestamp
	)
VALUES(
    coinName,
    confirmed_index,
    spent_index,
    spent,
    coinbase,
    puzzle_hash,
    address,
    coin_parent,
    amount,
    time_stamp
	)
ON CONFLICT (coin_name) 
DO UPDATE SET 
    confirmed_index = EXCLUDED.confirmed_index,
    spent_index = EXCLUDED.spent_index,
    spent = EXCLUDED.spent,
    coinbase = EXCLUDED.coinbase,
    puzzle_hash = EXCLUDED.puzzle_hash,
    address = EXCLUDED.address,
    coin_parent = EXCLUDED.coin_parent,
    amount = EXCLUDED.amount,
    timestamp = EXCLUDED.timestamp;

end;
$BODY$;


CREATE OR REPLACE PROCEDURE public.save_full_blocks_transactions_info_reward_claims_incorporated(
	IN headerHash character,
	IN parentCoinInfo character,
	IN puzzle_hash character,
	IN address character,
	IN amount numeric)
LANGUAGE 'plpgsql'
AS $BODY$


begin

INSERT INTO public.coin_record (
    header_hash,
    parent_coin_info,
    puzzle_hash,
    address,
    amount
	)
VALUES(
    headerHash,
    parentCoinInfo,
    puzzle_hash,
    address,
    amount
	)
ON CONFLICT (header_hash, parent_coin_info) 
DO UPDATE SET 
    puzzle_hash = EXCLUDED.puzzle_hash,
    address = EXCLUDED.address,
    amount = EXCLUDED.amount;

commit;
end;
$BODY$;

