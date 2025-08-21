import hashlib, json, time

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

class Block:
    def __init__(self, index, prev_hash, record, timestamp=None):
        self.index = index
        self.prev_hash = prev_hash
        self.record = record
        self.timestamp = timestamp or time.time()
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "prev_hash": self.prev_hash,
            "record": self.record,
            "timestamp": self.timestamp
        }, sort_keys=True)
        return sha256(block_string)

class MedicalBlockchain:
    def __init__(self, patient_name):
        self.patient_name = patient_name
        self.chain = []
        self.create_genesis()
  
    def create_genesis(self):
        genesis = Block(0, "0", {"msg": "Genesis Block - Patient Medical History"})
        self.chain.append(genesis)

    def add_record(self, doctor, diagnosis, prescription):
        record = {
            "Patient": self.patient_name,
            "Doctor": doctor,
            "Diagnosis": diagnosis,
            "Prescription": prescription
        }
        prev = self.chain[-1]
        new_block = Block(len(self.chain), prev.hash, record)
        self.chain.append(new_block)

    def get_medical_history(self):
        history = []
        for b in self.chain:
            if isinstance(b.record, dict) and b.record.get("Patient") == self.patient_name:
                history.append(b.record)
        return history


name = input("Enter patient name: ")
mb = MedicalBlockchain(name)

while True:
    print("\n1. Add Medical Record")
    print("2. Show Medical History")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        doctor = input("Doctor's Name: ")
        diagnosis = input("Diagnosis: ")
        prescription = input("Prescription: ")
        mb.add_record(doctor, diagnosis, prescription)
        print("✅ Record added successfully!")

    elif choice == "2":
        history = mb.get_medical_history()
        print(f"\n📋 Medical History of {mb.patient_name}:")
        for h in history:
            if "Doctor" in h:   # skip genesis
                print(h)

    elif choice == "3":
        print("Exiting... Goodbye!")
        break

    else:
        print("❌ Invalid choice, try again.")
