from django.db import models

class Block(models.Model):
    
    class Meta:
        db_table = 'full_blocks'

    header_hash = models.CharField(max_length=64, primary_key=True)
    weight = models.BigIntegerField()
    height = models.IntegerField()
    total_iters = models.BigIntegerField()
    signage_point_index = models.SmallIntegerField()
    pos_ss_cc_challenge_hash = models.CharField(max_length=64)
    proof_of_space_challenge = models.CharField(max_length=64)
    proof_of_space_pool_public_key = models.CharField(max_length=96)
    proof_of_space_pool_contract_puzzle_hash = models.CharField(max_length=64)
    proof_of_space_plot_public_key = models.CharField(max_length=96)
    proof_of_space_size = models.SmallIntegerField()
    proof_of_space_proof = models.BinaryField()
    challenge_chain_sp_vdf_challenge = models.CharField(max_length=64)
    challenge_chain_sp_vdf_number_of_iterations = models.BigIntegerField()
    challenge_chain_sp_vdf_output_data = models.CharField(max_length=200)
    challenge_chain_sp_signature = models.CharField(max_length=192)
    challenge_chain_ip_vdf_challenge = models.CharField(max_length=64)
    challenge_chain_ip_vdf_number_of_iterations = models.BigIntegerField()
    challenge_chain_ip_vdf_output_data = models.CharField(max_length=200)
    reward_chain_sp_vdf_challenge = models.CharField(max_length=64)
    reward_chain_sp_vdf_number_of_iterations = models.BigIntegerField()
    reward_chain_sp_vdf_output_data = models.CharField(max_length=200)
    reward_chain_sp_signature = models.CharField(max_length=192)
    reward_chain_ip_vdf_challenge = models.CharField(max_length=64)
    reward_chain_ip_vdf_number_of_iterations = models.BigIntegerField()
    reward_chain_ip_vdf_output_data = models.CharField(max_length=200)
    infused_challenge_chain_ip_vdf_challenge = models.CharField(max_length=64)
    infused_challenge_chain_ip_vdf_number_of_iterations = models.BigIntegerField()
    infused_challenge_chain_ip_vdf_output_data = models.CharField(max_length=200)
    is_tx_block = models.BooleanField()
    challenge_chain_sp_proof_witness_type = models.SmallIntegerField()
    challenge_chain_sp_proof_witness = models.BinaryField()
    challenge_chain_sp_proof_normalized_to_identity = models.BooleanField(),
    challenge_chain_ip_proof_witness_type = models.SmallIntegerField()
    challenge_chain_ip_proof_witness = models.BinaryField()
    challenge_chain_ip_proof_normalized_to_identity = models.BooleanField(),
    reward_chain_sp_proof_witness_type = models.SmallIntegerField()
    reward_chain_sp_proof_witness = models.BinaryField()
    reward_chain_sp_proof_normalized_to_identity = models.BooleanField(),
    reward_chain_ip_proof_witness_type = models.SmallIntegerField()
    reward_chain_ip_proof_witness = models.BinaryField()
    reward_chain_ip_proof_normalized_to_identity = models.BooleanField(),
    infused_challenge_chain_ip_proof_witness_type = models.SmallIntegerField()
    infused_challenge_chain_ip_proof_witness = models.BinaryField()
    infused_challenge_chain_ip_proof_normalized_to_identity = models.BooleanField(),
    prev_header_hash = models.CharField(max_length=64)
    reward_block_hash = models.CharField(max_length=64)
    foliage_block_data_unfinished_reward_block_hash = models.CharField(max_length=64)
    foliage_block_data_pool_target_puzzle_hash = models.CharField(max_length=64)
    foliage_block_data_pool_target_address = models.CharField(max_length=62)
    foliage_block_data_pool_target_max_height = models.SmallIntegerField()
    foliage_block_data_pool_signature = models.CharField(max_length=192)
    foliage_block_data_farmer_reward_puzzle_hash = models.CharField(max_length=64)
    foliage_block_data_farmer_reward_address = models.CharField(max_length=62)
    foliage_block_data_extension_data = models.CharField(max_length=64)
    foliage_block_data_signature = models.CharField(max_length=192)
    foliage_transaction_block_hash = models.CharField(max_length=64)
    foliage_transaction_block_signature = models.CharField(max_length=192)
    foliage_transaction_block_prev_transaction_block_hash = models.CharField(max_length=64)
    foliage_transaction_block_timestamp = models.BigIntegerField()
    foliage_transaction_block_filter_hash = models.CharField(max_length=64)
    foliage_transaction_block_additions_root = models.CharField(max_length=64)
    foliage_transaction_block_removals_root = models.CharField(max_length=64)
    foliage_transaction_block_transactions_info_hash = models.CharField(max_length=64)
    transactions_info_generator_root = models.CharField(max_length=64)
    transactions_info_generator_refs_root = models.CharField(max_length=64)
    transactions_info_aggregated_signature = models.CharField(max_length=192)
    transactions_info_fees = models.BigIntegerField()
    transactions_info_cost = models.BigIntegerField()
    dollar_price = models.BigIntegerField()

class Coin(models.Model):

    class Meta:
        db_table = 'coin_record'

    coin_name = models.CharField(max_length=64, primary_key=True)
    confirmed_index = models.BigIntegerField()
    spent_index = models.BigIntegerField()
    spent = models.IntegerField()
    coinbase = models.IntegerField()
    puzzle_hash = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    coin_parent = models.CharField(max_length=64)
    amount = models.BigIntegerField()

    