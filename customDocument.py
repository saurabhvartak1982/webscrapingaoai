class CustomDocument:
    def __init__(self, doc_id, content, title, source, metadata):
        self.id = doc_id
        self.page_content = content
        self.title = title
        self.source = source
        self.metadata = metadata