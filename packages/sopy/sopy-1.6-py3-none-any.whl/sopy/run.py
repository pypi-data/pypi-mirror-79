from sopy import Document

sop = Document("sops/sop.txt", template_location="sops")

sop.render_document(program_name="MS",
                    university_name="Stanford University", gizooglify=True)

sop.save_file("final_sop.txt")
