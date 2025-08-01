import psycopg2
from faker import Faker
import random
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# DB connection setup
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

fake = Faker()

# 1. Generate and insert vendors
def insert_vendors(n=10):
    for _ in range(n):
        vendor_name = fake.company()
        cursor.execute(
            "INSERT INTO public.vendors (vendor_name) VALUES (%s)",
            (vendor_name,)
        )
    conn.commit()

# 2. Generate and insert devices
def insert_devices(n=50):
    # Get vendor IDs
    cursor.execute("SELECT vendor_id FROM vendors")
    vendor_ids = [row[0] for row in cursor.fetchall()]

    categories = ["MRI Machine", "CT Scanner", "Infusion System", "X-Ray Machine", "Ultrasound", "Patient Monitor"]
    os_versions = ["Windows XP", "Windows 7", "Windows 10", "Ubuntu", "Red Hat"]

    for _ in range(n):
        name = fake.catch_phrase()
        category = random.choice(categories)
        vendor_id = random.choice(vendor_ids)
        os = random.choice(os_versions)
        mds2 = random.choice([True, False])
        phi = random.choice([True, False])
        subnet = fake.ipv4(network=True)
        site = fake.city()
        risk_score = random.choice([10, 15, 20, 25])  # Simulate risk scores
        profiles = random.randint(1, 10)              # Simulate profile count

        cursor.execute("""
            INSERT INTO devices 
            (name, category, vendor_id, os, mds2_compliant, phi_flag, subnet, site, risk_score, profiles) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, category, vendor_id, os, mds2, phi, subnet, site, risk_score, profiles))

    conn.commit()




def insert_device_usage():
    cursor.execute("SELECT device_id FROM devices")
    device_ids = [row[0] for row in cursor.fetchall()]

    statuses = ["Used", "OnlineNotUsed", "Offline"]

    for device_id in device_ids:
        status = random.choice(statuses)
        cursor.execute("""
            INSERT INTO device_usage (device_id, usage_status)
            VALUES (%s, %s)
        """, (device_id, status))

    conn.commit()

def insert_recalls():
    cursor.execute("SELECT device_id FROM devices")
    device_ids = [row[0] for row in cursor.fetchall()]
    
    for device_id in random.sample(device_ids, k=int(len(device_ids) * 0.3)):  # 30% recalled
        reason = fake.sentence(nb_words=6)
        date = fake.date_this_year()
        cursor.execute("""
            INSERT INTO recalls (device_id, recall_reason, date_flagged)
            VALUES (%s, %s, %s)
        """, (device_id, reason, date))

    conn.commit()

def insert_compliance():
    cursor.execute("SELECT device_id FROM devices")
    device_ids = [row[0] for row in cursor.fetchall()]

    for device_id in device_ids:
        endpoint_protection = random.choice([True, False])
        eol_os = random.choice([True, False])
        cursor.execute("""
            INSERT INTO compliance (device_id, endpoint_protection, eol_os)
            VALUES (%s, %s, %s)
        """, (device_id, endpoint_protection, eol_os))

    conn.commit()

cursor.execute("DELETE FROM compliance")
cursor.execute("DELETE FROM recalls")
cursor.execute("DELETE FROM device_usage")
cursor.execute("DELETE FROM devices")
cursor.execute("DELETE FROM vendors")
conn.commit()


# Run 
insert_vendors()
insert_devices()
insert_device_usage()
insert_recalls()
insert_compliance()

cursor.close()
conn.close()
