"""Module containing the document templates with the section structures, and the questions to
answer in each section."""


im_template = {
    "document_title": "Investment Memo",
    "sections": [
        {
            "type": "title",
            "content": "Company Overview",
            "level": 1,
        },
        {
            "type": "text",
            "description": "Provides an overview of the company.",
            "prompts": [
                "What is the company industry?",
                "What are the company products or services?",
            ],
            "content": ""
        },
        {
            "type": "title",
            "content": "Market Analysis",
            "level": 1,
        },
        {
            "type": "text",
            "description": "Provides an analysis of the market.",
            "prompts": [
            ],
            "content": "",
        },
        {
            "type": "title",
            "content": "Product or Service Analysis",
            "level": 1,
        },
        {
            "type": "text",
            "description": "Provides an analysis of the company's products or services.",
            "prompts": [
                "What are the company's key products or services?",
            ],
            "content": "",
        }
    ]
}


im_template_full = {
    "document_title": "Investment Memo",
    "sections": [
        {
            "type": "title",
            "content": "Company Overview",
            "level": 1,
        },
        {
            "type": "text",
            "description": "Provides an overview of the company.",
            "prompts": [
                "What is the company name?",
                "What is the company industry?",
                "What are the company products or services?",
                "What is the company founding story and history?",
                "Provide an overview of the management team and key personnel.",
                "Add any other relevant information about the company, relevant for this overview.",
            ],
            "content": ""
        },
        {
            "type": "title",
            "content": "Market Analysis",
            "level": 1,
        },
        {
            "type": "text",
            "description": "Provides an analysis of the market.",
            "prompts": [
                "What is the company's target market?",
                "Who are the company's competitors?",
                "What is the company's competitive advantage?",
                "What are the market trends and growth opportunities?",
            ],
            "content": "",
        },
        {
            "type": "title",
            "content": "Product or Service Analysis",
            "level": 1,
        },
        {
            "type": "text",
            "description": "Provides an analysis of the company's products or services.",
            "prompts": [
                "What are the company's key products or services?",
                "What are the unique selling points (USPs) of the company's products or services?",
                "What are the product or service development plans?",
                "What are the product or service pricing strategies?",
                "What are the product or service distribution channels?",
            ],
            "content": "",
        },
    ]
}
