import json
import requests
import time

# Load SBOM
with open('/Users/jie/Desktop/OpenCode_Proj/orca-sbom-handoff/01_sbom_vex/output/sbom.cdx.json') as f:
    sbom = json.load(f)

# Prepare OSV querybatch
queries = []
for comp in sbom['components']:
    purl = comp.get('purl', '')
    if purl:
        queries.append({"purl": purl})

payload = {"queries": queries}
print(f"Querying OSV for {len(queries)} packages...")

# Query OSV
response = requests.post('https://api.osv.dev/v1/querybatch', json=payload, timeout=30)
response.raise_for_status()
result = response.json()

# Save raw response
with open('/Users/jie/Desktop/OpenCode_Proj/orca-sbom-handoff/01_sbom_vex/output/osv_query_batch.json', 'w') as f:
    json.dump(result, f, indent=2)

# Process results
results = result.get('results', [])
total_vulns = 0
for i, r in enumerate(results):
    vulns = r.get('vulns', [])
    comp_name = sbom['components'][i]['name']
    print(f"{comp_name}: {len(vulns)} vulnerabilities")
    total_vulns += len(vulns)
    for v in vulns:
        print(f"  - {v['id']}: {v.get('summary', 'N/A')[:80]}")

print(f"\nTotal vulnerabilities found: {total_vulns}")
