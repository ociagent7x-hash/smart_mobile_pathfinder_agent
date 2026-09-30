from generator import generate_local_documents, upload_to_oci_bucket

# 1. Generate dummy local PDF and DOCX files
pdf, docx = generate_local_documents("Principal Architect", "Oracle", "Sample Resume Content", "Sample Cover Letter Content")
print(f"Generated locally:\n - {pdf}\n - {docx}")

# 2. Upload to your OCI bucket and get PAR links
pdf_url = upload_to_oci_bucket(pdf)
docx_url = upload_to_oci_bucket(docx)

print(f"\nOCI PAR Download Links:")
print(f"PDF Link: {pdf_url}")
print(f"DOCX Link: {docx_url}")