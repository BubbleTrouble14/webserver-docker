from dataclasses import dataclass
from typing import Optional

from chia.types.blockchain_format.slots import (
    ChallengeChainSubSlot,
    InfusedChallengeChainSubSlot,
    RewardChainSubSlot,
    SubSlotProofs,
)
from chia.util.streamable import Streamable, streamable


@dataclass(frozen=True)
@streamable
class EndOfSubSlotBundle(Streamable):
    challenge_chain: ChallengeChainSubSlot
    infused_challenge_chain: Optional[InfusedChallengeChainSubSlot]
    reward_chain: RewardChainSubSlot
    proofs: SubSlotProofs

    def challenge_chain_infused_challenge_chain_sub_slot_hash(self):
        if(self.challenge_chain.infused_challenge_chain_sub_slot_hash is not None):
            return self.challenge_chain.infused_challenge_chain_sub_slot_hash.hex()
        return None

    def challenge_chain_subepoch_summary_hash(self):
        if(self.challenge_chain.subepoch_summary_hash is not None):
            return self.challenge_chain.subepoch_summary_hash.hex()
        return None

    def challenge_chain_new_sub_slot_iters(self):
        if(self.challenge_chain.new_sub_slot_iters is not None):
            return self.challenge_chain.new_sub_slot_iters
        return None

    def challenge_chain_new_difficulty(self):
        if(self.challenge_chain.new_difficulty is not None):
            return self.challenge_chain.new_difficulty
        return None



    def infused_challenge_chain_end_of_slot_vdf_challange(self):
        if(self.infused_challenge_chain is not None):
            return self.infused_challenge_chain.infused_challenge_chain_end_of_slot_vdf.challenge.hex()
        return None

    def infused_challenge_chain_end_of_slot_vdf_number_of_iterations(self):
        if(self.infused_challenge_chain is not None):
            return self.infused_challenge_chain.infused_challenge_chain_end_of_slot_vdf.number_of_iterations
        return None

    def infused_challenge_chain_end_of_slot_vdf_output_data(self):
        if(self.infused_challenge_chain is not None):
            return self.infused_challenge_chain.infused_challenge_chain_end_of_slot_vdf.output.data.hex()
        return None



    def reward_chain_infused_challenge_chain_sub_slot_hash(self):
        if(self.reward_chain.infused_challenge_chain_sub_slot_hash is not None):
            return self.reward_chain.infused_challenge_chain_sub_slot_hash.hex()
        return None



    def proofs_infused_challenge_chain_slot_proof_witness_type(self):
        if(self.proofs.infused_challenge_chain_slot_proof is not None):
            return self.proofs.infused_challenge_chain_slot_proof.witness_type
        return None

    def proofs_infused_challenge_chain_slot_proof_witness(self):
        if(self.proofs.infused_challenge_chain_slot_proof is not None):
            return self.proofs.infused_challenge_chain_slot_proof.witness
        return None

    def proofs_infused_challenge_chain_slot_proof_norm_to_identity(self):
        if(self.proofs.infused_challenge_chain_slot_proof is not None):
            return self.proofs.infused_challenge_chain_slot_proof.normalized_to_identity
        return None