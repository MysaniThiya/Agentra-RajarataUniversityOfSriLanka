
import json

from agents.email_analysis_agent import analyze_email


test_emails = [

    {
        "sender": "colleague@gmail.com",
        "subject": "Meeting schedule for tomorrow",
        "body": """
        Hello,

        Our meeting is scheduled for tomorrow at 10 AM.
        Please review the attached meeting notes.

        Best regards,
        John
        """
    },

    {
        "sender": "security@example-bank.com",
        "subject": "URGENT: Verify your account immediately",
        "body": """
        Dear Customer,

        Your bank account will be suspended today.
        Click the link below immediately and verify your password.

        Thank you,
        Bank Security Team
        """
    },

    {
        "sender": "offers@example.com",
        "subject": "Special discount offer",
        "body": """
        Congratulations!

        Get 50 percent off on our products.
        Subscribe to our newsletter to receive more offers.
        """
    }
]


for index, email in enumerate(test_emails, start=1):

    print(f"\n========== EMAIL {index} ==========")

    result = analyze_email(email)

    print(
        json.dumps(
            result.model_dump(),
            indent=4
        )
    )
