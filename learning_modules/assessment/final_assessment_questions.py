#!/usr/bin/env python3
"""
Final Assessment Questions Pool
40 questions covering all modules for comprehensive assessment
"""

class FinalAssessmentQuestions:
    """Final Assessment Questions Pool - 40 questions total"""
    
    @classmethod
    def get_question_pool(cls):
        """Get all 40 questions for the final assessment pool"""
        return [
            # Module 1: What is Social Engineering (8 questions)
            {
                "question_text": "What is the primary goal of social engineering attacks?",
                "option_a": "To gain unauthorized access to computer systems",
                "option_b": "To manipulate people into revealing confidential information",
                "option_c": "To spread malware through email attachments",
                "option_d": "To create fake websites for phishing",
                "correct_answer": "b",
                "explanation": "Social engineering attacks primarily focus on manipulating human psychology to extract confidential information, rather than directly attacking technical systems.",
                "question_set": 1,
                "module_source": "Module 1"
            },
            {
                "question_text": "Which of the following is NOT a common social engineering technique?",
                "option_a": "Phishing",
                "option_b": "Pretexting",
                "option_c": "SQL Injection",
                "option_d": "Baiting",
                "correct_answer": "c",
                "explanation": "SQL Injection is a technical attack method, not a social engineering technique. Social engineering focuses on human manipulation.",
                "question_set": 1,
                "module_source": "Module 1"
            },
            {
                "question_text": "What makes social engineering attacks particularly dangerous?",
                "option_a": "They are difficult to detect",
                "option_b": "They exploit human psychology",
                "option_c": "They bypass technical security measures",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Social engineering is dangerous because it exploits human psychology, bypasses technical security, and is often difficult to detect.",
                "question_set": 1,
                "module_source": "Module 1"
            },
            {
                "question_text": "Which psychological principle is most commonly exploited in social engineering?",
                "option_a": "Authority",
                "option_b": "Urgency",
                "option_c": "Trust",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Social engineers exploit multiple psychological principles including authority, urgency, and trust to manipulate victims.",
                "question_set": 1,
                "module_source": "Module 1"
            },
            {
                "question_text": "What is the first line of defense against social engineering?",
                "option_a": "Strong passwords",
                "option_b": "Antivirus software",
                "option_c": "Security awareness training",
                "option_d": "Firewalls",
                "correct_answer": "c",
                "explanation": "Security awareness training is the first line of defense as it educates users to recognize and resist social engineering attempts.",
                "question_set": 1,
                "module_source": "Module 1"
            },
            {
                "question_text": "Which of the following is a red flag for social engineering?",
                "option_a": "Requests for immediate action",
                "option_b": "Unsolicited contact",
                "option_c": "Requests for sensitive information",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "All these behaviors are red flags that may indicate a social engineering attempt.",
                "question_set": 1,
                "module_source": "Module 1"
            },
            {
                "question_text": "What should you do if you suspect a social engineering attempt?",
                "option_a": "Ignore it",
                "option_b": "Report it to your security team",
                "option_c": "Respond to verify the request",
                "option_d": "Forward it to colleagues",
                "correct_answer": "b",
                "explanation": "Suspected social engineering attempts should be reported to the security team immediately for investigation.",
                "question_set": 1,
                "module_source": "Module 1"
            },
            {
                "question_text": "Which factor makes social engineering attacks more likely to succeed?",
                "option_a": "Lack of security awareness",
                "option_b": "High stress situations",
                "option_c": "Trust in authority figures",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "All these factors can make individuals more vulnerable to social engineering attacks.",
                "question_set": 1,
                "module_source": "Module 1"
            },
            
            # Module 2: Phishing (8 questions)
            {
                "question_text": "What is the most common type of phishing attack?",
                "option_a": "Spear phishing",
                "option_b": "Email phishing",
                "option_c": "Whaling",
                "option_d": "Vishing",
                "correct_answer": "b",
                "explanation": "Email phishing is the most common type, targeting large numbers of users with generic messages.",
                "question_set": 1,
                "module_source": "Module 2"
            },
            {
                "question_text": "Which of the following is a sign of a phishing email?",
                "option_a": "Generic greeting",
                "option_b": "Urgent action required",
                "option_c": "Suspicious sender address",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "All these characteristics are common indicators of phishing emails.",
                "question_set": 1,
                "module_source": "Module 2"
            },
            {
                "question_text": "What should you do before clicking a link in an email?",
                "option_a": "Click immediately",
                "option_b": "Hover over the link to check the URL",
                "option_c": "Forward to colleagues",
                "option_d": "Reply to the sender",
                "correct_answer": "b",
                "explanation": "Hovering over a link reveals the actual destination URL, helping identify suspicious links.",
                "question_set": 1,
                "module_source": "Module 2"
            },
            {
                "question_text": "What is spear phishing?",
                "option_a": "Generic phishing emails",
                "option_b": "Targeted phishing against specific individuals",
                "option_c": "Phishing via phone calls",
                "option_d": "Phishing via text messages",
                "correct_answer": "b",
                "explanation": "Spear phishing is a targeted attack against specific individuals, often using personal information.",
                "question_set": 1,
                "module_source": "Module 2"
            },
            {
                "question_text": "Which of the following is NOT a type of phishing?",
                "option_a": "Vishing",
                "option_b": "Smishing",
                "option_c": "Pharming",
                "option_d": "Spamming",
                "correct_answer": "d",
                "explanation": "Spamming is sending unsolicited bulk messages, not a type of phishing attack.",
                "question_set": 1,
                "module_source": "Module 2"
            },
            {
                "question_text": "What is the best way to verify a suspicious email?",
                "option_a": "Reply to the email",
                "option_b": "Contact the sender through official channels",
                "option_c": "Click on the links",
                "option_d": "Forward to all contacts",
                "correct_answer": "b",
                "explanation": "Contact the sender through official, verified channels to confirm the legitimacy of the request.",
                "question_set": 1,
                "module_source": "Module 2"
            },
            {
                "question_text": "What should you do if you receive a suspicious attachment?",
                "option_a": "Open it immediately",
                "option_b": "Delete it without opening",
                "option_c": "Forward it to IT",
                "option_d": "Save it for later",
                "correct_answer": "b",
                "explanation": "Suspicious attachments should be deleted immediately without opening to prevent malware infection.",
                "question_set": 1,
                "module_source": "Module 2"
            },
            {
                "question_text": "Which of the following is a red flag in a phishing email?",
                "option_a": "Poor grammar and spelling",
                "option_b": "Requests for personal information",
                "option_c": "Threats of account closure",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "All these characteristics are common red flags in phishing emails.",
                "question_set": 1,
                "module_source": "Module 2"
            },
            
            # Module 3: Fortifying Your Accounts (8 questions)
            {
                "question_text": "What is the minimum recommended length for a strong password?",
                "option_a": "6 characters",
                "option_b": "8 characters",
                "option_c": "12 characters",
                "option_d": "16 characters",
                "correct_answer": "c",
                "explanation": "A minimum of 12 characters is recommended for strong passwords to resist brute force attacks.",
                "question_set": 1,
                "module_source": "Module 3"
            },
            {
                "question_text": "Which of the following makes a password stronger?",
                "option_a": "Using personal information",
                "option_b": "Using dictionary words",
                "option_c": "Using a mix of characters, numbers, and symbols",
                "option_d": "Using the same password for multiple accounts",
                "correct_answer": "c",
                "explanation": "A strong password should include a mix of uppercase, lowercase, numbers, and special characters.",
                "question_set": 1,
                "module_source": "Module 3"
            },
            {
                "question_text": "What is Multi-Factor Authentication (MFA)?",
                "option_a": "Using multiple passwords",
                "option_b": "Using two or more verification methods",
                "option_c": "Using biometric authentication only",
                "option_d": "Using the same password twice",
                "correct_answer": "b",
                "explanation": "MFA requires two or more verification methods (something you know, have, or are) for authentication.",
                "question_set": 1,
                "module_source": "Module 3"
            },
            {
                "question_text": "Which of the following is NOT a good password practice?",
                "option_a": "Using unique passwords for each account",
                "option_b": "Sharing passwords with trusted colleagues",
                "option_c": "Using a password manager",
                "option_d": "Regularly updating passwords",
                "correct_answer": "b",
                "explanation": "Passwords should never be shared, even with trusted colleagues, as this creates security risks.",
                "question_set": 1,
                "module_source": "Module 3"
            },
            {
                "question_text": "What is the purpose of a password manager?",
                "option_a": "To store passwords securely",
                "option_b": "To generate strong passwords",
                "option_c": "To autofill login forms",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Password managers help store, generate, and autofill strong passwords securely.",
                "question_set": 1,
                "module_source": "Module 3"
            },
            {
                "question_text": "Which of the following is a sign of a compromised account?",
                "option_a": "Unexpected login notifications",
                "option_b": "Changes to account settings you didn't make",
                "option_c": "Unfamiliar activity in account history",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "All these signs may indicate that an account has been compromised.",
                "question_set": 1,
                "module_source": "Module 3"
            },
            {
                "question_text": "What should you do if you suspect your account is compromised?",
                "option_a": "Change your password immediately",
                "option_b": "Enable MFA if not already active",
                "option_c": "Check for unauthorized activity",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "If you suspect account compromise, change passwords, enable MFA, and check for unauthorized activity.",
                "question_set": 1,
                "module_source": "Module 3"
            },
            {
                "question_text": "Which of the following is the most secure authentication method?",
                "option_a": "Password only",
                "option_b": "Password + SMS",
                "option_c": "Password + authenticator app",
                "option_d": "Biometric only",
                "correct_answer": "c",
                "explanation": "Password + authenticator app provides the strongest security as authenticator apps are more secure than SMS.",
                "question_set": 1,
                "module_source": "Module 3"
            },
            
            # Module 4: Immediate Action After a Suspected Attack (8 questions)
            {
                "question_text": "What is the first step when you suspect a social engineering attack?",
                "option_a": "Continue working normally",
                "option_b": "Disconnect from the network immediately",
                "option_c": "Change all passwords",
                "option_d": "Report to security team",
                "correct_answer": "b",
                "explanation": "The first step is to disconnect from the network to prevent further damage or data exfiltration.",
                "question_set": 1,
                "module_source": "Module 4"
            },
            {
                "question_text": "Who should you notify first about a suspected attack?",
                "option_a": "Your manager",
                "option_b": "IT Security team",
                "option_c": "Your colleagues",
                "option_d": "The attacker",
                "correct_answer": "b",
                "explanation": "The IT Security team should be notified first as they are trained to handle security incidents.",
                "question_set": 1,
                "module_source": "Module 4"
            },
            {
                "question_text": "What information should you document about the incident?",
                "option_a": "Time and date of the incident",
                "option_b": "Details of what happened",
                "option_c": "Any suspicious communications",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Document all relevant details including time, date, what happened, and any communications for investigation.",
                "question_set": 1,
                "module_source": "Module 4"
            },
            {
                "question_text": "What should you do with suspicious emails after reporting?",
                "option_a": "Delete them immediately",
                "option_b": "Forward them to colleagues",
                "option_c": "Keep them for evidence",
                "option_d": "Reply to the sender",
                "correct_answer": "c",
                "explanation": "Keep suspicious emails as evidence for the security team's investigation.",
                "question_set": 1,
                "module_source": "Module 4"
            },
            {
                "question_text": "Which of the following should you NOT do after a suspected attack?",
                "option_a": "Change passwords",
                "option_b": "Continue using the same devices",
                "option_c": "Report the incident",
                "option_d": "Document the incident",
                "correct_answer": "b",
                "explanation": "You should not continue using potentially compromised devices until they are checked by IT security.",
                "question_set": 1,
                "module_source": "Module 4"
            },
            {
                "question_text": "What is the purpose of incident response procedures?",
                "option_a": "To minimize damage",
                "option_b": "To preserve evidence",
                "option_c": "To prevent future attacks",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Incident response procedures help minimize damage, preserve evidence, and prevent future attacks.",
                "question_set": 1,
                "module_source": "Module 4"
            },
            {
                "question_text": "When should you change your passwords after a suspected attack?",
                "option_a": "Never",
                "option_b": "Only if requested by IT",
                "option_c": "Immediately after disconnecting",
                "option_d": "After 24 hours",
                "correct_answer": "c",
                "explanation": "Change passwords immediately after disconnecting to prevent further unauthorized access.",
                "question_set": 1,
                "module_source": "Module 4"
            },
            {
                "question_text": "What should you do if you accidentally clicked a malicious link?",
                "option_a": "Ignore it",
                "option_b": "Report it immediately and disconnect",
                "option_c": "Continue browsing",
                "option_d": "Share with colleagues",
                "correct_answer": "b",
                "explanation": "If you clicked a malicious link, report it immediately and disconnect from the network to prevent further damage.",
                "question_set": 1,
                "module_source": "Module 4"
            },
            
            # Module 5: The Evolving Threat Landscape (8 questions)
            {
                "question_text": "What is the main reason social engineering attacks are evolving?",
                "option_a": "Technology advances",
                "option_b": "Increased security awareness",
                "option_c": "Both A and B",
                "option_d": "Neither A nor B",
                "correct_answer": "c",
                "explanation": "Social engineering evolves due to both technological advances and increased security awareness, requiring attackers to adapt.",
                "question_set": 1,
                "module_source": "Module 5"
            },
            {
                "question_text": "Which of the following is an emerging social engineering threat?",
                "option_a": "Deepfake technology",
                "option_b": "AI-generated content",
                "option_c": "Voice cloning",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "All these technologies represent emerging threats that can be used for social engineering attacks.",
                "question_set": 1,
                "module_source": "Module 5"
            },
            {
                "question_text": "What is the best way to stay protected against evolving threats?",
                "option_a": "Regular security training",
                "option_b": "Keeping software updated",
                "option_c": "Following security best practices",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Protection against evolving threats requires continuous training, updates, and following security best practices.",
                "question_set": 1,
                "module_source": "Module 5"
            },
            {
                "question_text": "Which of the following is a future trend in social engineering?",
                "option_a": "More sophisticated AI attacks",
                "option_b": "Increased use of social media",
                "option_c": "Targeting of IoT devices",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Future trends include AI-powered attacks, social media exploitation, and targeting of Internet of Things devices.",
                "question_set": 1,
                "module_source": "Module 5"
            },
            {
                "question_text": "What role does social media play in modern social engineering?",
                "option_a": "Provides personal information for targeting",
                "option_b": "Enables mass communication",
                "option_c": "Creates trust through connections",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Social media provides attackers with personal information, mass communication tools, and ways to build trust.",
                "question_set": 1,
                "module_source": "Module 5"
            },
            {
                "question_text": "How can organizations prepare for future social engineering threats?",
                "option_a": "Invest in security awareness training",
                "option_b": "Implement advanced security technologies",
                "option_c": "Develop incident response plans",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Organizations need comprehensive preparation including training, technology, and response planning.",
                "question_set": 1,
                "module_source": "Module 5"
            },
            {
                "question_text": "What is the importance of continuous learning in cybersecurity?",
                "option_a": "Threats are constantly evolving",
                "option_b": "New attack methods emerge regularly",
                "option_c": "Security practices need updating",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Continuous learning is essential because threats, attack methods, and security practices are constantly evolving.",
                "question_set": 1,
                "module_source": "Module 5"
            },
            {
                "question_text": "Which of the following is a key principle for future cybersecurity?",
                "option_a": "Assume breach mentality",
                "option_b": "Zero trust architecture",
                "option_c": "Defense in depth",
                "option_d": "All of the above",
                "correct_answer": "d",
                "explanation": "Future cybersecurity relies on assuming breaches can happen, implementing zero trust, and using multiple defense layers.",
                "question_set": 1,
                "module_source": "Module 5"
            }
        ]
    
    @classmethod
    def get_random_questions(cls, count=25):
        """Get random questions from the pool"""
        import random
        questions = cls.get_question_pool()
        if len(questions) <= count:
            return questions
        return random.sample(questions, count)
    
    @classmethod
    def get_questions_by_module(cls, module_source):
        """Get questions filtered by module source"""
        questions = cls.get_question_pool()
        return [q for q in questions if q['module_source'] == module_source]

