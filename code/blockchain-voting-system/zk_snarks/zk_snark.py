import subprocess
import json

class ZkSnark:
    @staticmethod
    def generate_proof():
        """Generates a zk-SNARK proof"""
        subprocess.run(["zokrates", "compute-witness", "-a", "4", "6"], check=True)
        subprocess.run(["zokrates", "generate-proof"], check=True)

        with open("proof.json", "r") as f:
            return json.load(f)

    @staticmethod
    def verify_proof():
        """Verifies the zk-SNARK proof"""
        result = subprocess.run(["zokrates", "verify"], capture_output=True, text=True)
        return "PASSED" in result.stdout

# to test zokratis is working
# python3 -c "from zk_snark import ZkSnark; print(ZkSnark.generate_proof()); print('Verification:', ZkSnark.verify_proof())"
