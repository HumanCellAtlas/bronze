from bronze.libs.google.docs import doc as gdoc
from bronze.libs.google import drive as gdrive
from typing import Union


def create_doc_from_template(
    template_url: str,
    service_account_key: Union[str, dict],
    copy_title: str = None,
    **template_vars,
) -> str:
    """Create a doc and render it from the template Google document."""
    # Step 1: Define the transaction
    requests = []
    for key, val in template_vars.items():
        requests.append(
            {
                'replaceAllText': {
                    'containsText': {
                        'text': "{{" + str(key) + "}}",
                        'matchCase': 'true',
                    },
                    'replaceText': val,
                }
            }
        )

    # Step 2: Copy the file and get the result fileid
    drive = gdrive.DriveAdmin(service_account_key=service_account_key)
    duplicated_doc = drive.duplicateDocument(
        document_url=template_url, copy_title=copy_title
    )
    duplicated_doc_id = duplicated_doc['id']
    print(f"Document {duplicated_doc['name']} has been created!")

    # Step 3: Execute the transaction
    doc_admin = gdoc.DocAdmin(service_account_key=service_account_key)
    doc_admin.updateDocument(
        document_identifier=duplicated_doc_id, update_requests=requests
    )
    print(f"Document {duplicated_doc['name']} has been updated!")
    return duplicated_doc_id
