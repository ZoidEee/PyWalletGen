from typing import Dict, Any
from bitcoinlib.wallets import Wallet, wallet_exists, wallet_delete


class BTCWalletGeneration:
    def __init__(self, wallet_name: str):
        self.wallet_name = wallet_name

        if wallet_exists(self.wallet_name):
            self._delete_existing_wallet()
        else:
            print(f"Wallet '{self.wallet_name}' does not exist.")

    def _delete_existing_wallet(self):
        try:
            if wallet_delete(self.wallet_name, force=True):
                print(f"Wallet '{self.wallet_name}' has been deleted successfully.")
            else:
                print(f"Error deleting wallet '{self.wallet_name}'.")
        except Exception as e:
            print(f"Exception occurred while deleting wallet: {e}")

    def _create_wallet(self, network: str, witness_type: str) -> Dict[str, Any]:
        try:
            wallet = Wallet.create(
                self.wallet_name, network=network, witness_type=witness_type
            )
            wallet_key = wallet.get_key()
            print(
                f"name: {wallet.name}\n"
                f"type: {witness_type}\n"
                f"address: {wallet_key.address}\n"
                f"private_key: {wallet_key.wif}\n"
                f"public_key: {wallet_key.key().public_hex}"
            )
            return {
                "name": wallet.name,
                "type": witness_type,
                "address": wallet_key.address,
                "private_key": wallet_key.wif,
                "public_key": wallet_key.key().public_hex,
            }
        except Exception as e:
            print(f"Exception occurred while creating wallet: {e}")
            return {}

    def legacy_wallet(self) -> Dict[str, Any]:
        return self._create_wallet("bitcoin", "legacy")

    def native_segwit(self) -> Dict[str, Any]:
        return self._create_wallet("bitcoin", "segwit")

    def p2sh_segwit(self) -> Dict[str, Any]:
        return self._create_wallet("bitcoin", "p2sh-segwit")

    def testnet_wallet(self) -> Dict[str, Any]:
        return self._create_wallet("testnet", "legacy")

    def hd_wallet(self, derivation_path: str = "m/44'/0'/0'/0") -> Dict[str, Any]:
        try:
            wallet = Wallet.create(
                self.wallet_name, network="bitcoin", key_path=derivation_path
            )
            wallet_key = wallet.get_key()
            return {
                "name": wallet.name,
                "derivation_path": wallet.key_path,
                "address": wallet_key.address,
                "private_key": wallet_key.wif,
                "public_key": wallet_key.key().public_hex,
            }
        except Exception as e:
            print(f"Exception occurred while creating HD wallet: {e}")
            return {}
