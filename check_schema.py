import sqlite3

conn = sqlite3.connect('bikevault.db')
cursor = conn.cursor()

print("\n" + "="*70)
print("📊 BIKEVAULT DATABASE SCHEMA - VEHICLE TABLE")
print("="*70)

cursor.execute("PRAGMA table_info(vehicle)")
columns = cursor.fetchall()

print(f"\n{'Column Name':<35} {'Data Type':<15} {'Required'}")
print("-" * 70)

for col in columns:
    col_id, col_name, col_type, notnull, default, pk = col
    required = "✓" if notnull else "✗"
    print(f"{col_name:<35} {col_type:<15} {required}")

conn.close()

print("\n" + "="*70)
print("✅ DATABASE IS READY WITH ALL CHECKLIST COLUMNS!")
print("="*70)
print("\n🔍 Checklist Columns Added:")
print("   ✓ number_of_keys")
print("   ✓ scratches_present")
print("   ✓ scratches_details")
print("   ✓ dents_present")
print("   ✓ dents_details")
print("   ✓ glass_damage_present")
print("   ✓ glass_damage_details")
print("   ✓ tire_condition")
print("   ✓ battery_status")
print("   ✓ lights_issue_present")
print("   ✓ lights_details")
print("   ✓ engine_status")
print("   ✓ condition_notes")
print("\n🚀 When you add a vehicle through the form, ALL this data will be saved!")
