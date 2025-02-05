### ** README.md – Setting Up ZoKrates & Running a Test**
Basic setup instructions for running **ZoKrates** in our blockchain-based quadratic voting project.

---

## ** Prerequisites**
Before running the test, ensure you have the following installed:

### **1. Install ZoKrates**
Run the following command to install ZoKrates:

```bash
curl -LSfs get.zokrat.es | sh
```

Verify installation:

```bash
zokrates --version
```

 Expected output:
```
ZoKrates X.X.X
```

---

## ** Setting Up ZoKrates**
1. **Navigate to the zk-SNARKs directory:**
   ```bash
   cd zk_snarks
   ```

2. **Compile the circuit:**
   ```bash
   zokrates compile -i circuit.zok
   ```

3. **Generate proving and verification keys:**
   ```bash
   zokrates setup
   ```

4. **Compute witness for test inputs (`x = 4, y = 6`):**
   ```bash
   zokrates compute-witness -a 4 6
   ```

5. **Generate a zk-SNARK proof:**
   ```bash
   zokrates generate-proof
   ```

6. **Verify the proof:**
   ```bash
   zokrates verify
   ```

 Expected output:
```
Performing verification...
PASSED
```

---

## ** Running the Python Test**
1. **Run the test script:**
   ```bash
   python3 zk_snark.py
   ```

 Expected output:
```
Proof generated: { ... }
Verification: True
```

---

## ** Summary**
This guide ensures that **ZoKrates is properly set up** and that zk-SNARK proof generation and verification **work correctly**.

If you run into any issues, try:
```bash
rm -rf proof.json verification.key proving.key witness
```
Then **re-run the steps**.

---

Your zk-SNARK setup is now complete! 

