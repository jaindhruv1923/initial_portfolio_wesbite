# Multilingual Test Corpus — Kavach

> Purpose: evaluation data for the security engine's PII/secret detection across languages.
> All PAN/Aadhaar/phone/account/email values below are FAKE, for testing only. Never use real
> data. This corpus is balanced between sensitive and non-sensitive examples per language so
> precision, recall, and F1 can be measured meaningfully — not just "did it catch everything"
> but also "did it wrongly flag safe text."

## Format
| ID | Text | Sensitive? | Entity type |
|----|------|------------|-------------|

---

## Hindi (10 examples)
| ID | Text | Sensitive? | Entity type |
|----|------|------------|-------------|
| HI-01 | मेरा PAN नंबर ABCDE1234F है | Yes | PAN |
| HI-02 | मुझे लोन के बारे में जानकारी चाहिए | No | — |
| HI-03 | मेरा आधार नंबर 1234 5678 9012 है, कृपया वेरिफाई करें | Yes | Aadhaar-like |
| HI-04 | कृपया मुझे 9876543210 पर कॉल करें | Yes | Phone number |
| HI-05 | मेरा नाम राहुल है और मैं दिल्ली में रहता हूँ | No | — |
| HI-06 | मेरा बैंक खाता नंबर 112233445566 है, पैसे भेजिए | Yes | Bank account |
| HI-07 | कल की मीटिंग कितने बजे है? | No | — |
| HI-08 | मेरा ईमेल rahul.demo123@example.com है | Yes | Email |
| HI-09 | ग्राहक सेवा का समय क्या है? | No | — |
| HI-10 | मेरा PAN card ABCDE1234F खो गया है, नया कैसे बनवाऊं | Yes | PAN |

## Marathi (10 examples)
| ID | Text | Sensitive? | Entity type |
|----|------|------------|-------------|
| MR-01 | माझा PAN नंबर ABCDE1234F आहे | Yes | PAN |
| MR-02 | माझे खाते कधी उघडले? | No | — |
| MR-03 | माझा आधार क्रमांक 1234 5678 9012 आहे | Yes | Aadhaar-like |
| MR-04 | कृपया मला 9876543210 वर संपर्क करा | Yes | Phone number |
| MR-05 | माझं नाव सुमित आहे, मी पुण्यात राहतो | No | — |
| MR-06 | माझा बँक खाते क्रमांक 112233445566 आहे | Yes | Bank account |
| MR-07 | उद्याची सुट्टी आहे का? | No | — |
| MR-08 | माझा ईमेल sumit.demo@example.com आहे | Yes | Email |
| MR-09 | ऑफिस किती वाजता उघडते? | No | — |
| MR-10 | माझं PAN कार्ड हरवलं, नवीन कसं मिळेल | Yes | PAN |

## Tamil (10 examples)
| ID | Text | Sensitive? | Entity type |
|----|------|------------|-------------|
| TA-01 | என் PAN number ABCDE1234F | Yes | PAN |
| TA-02 | எனக்கு கடன் பற்றி தெரிந்து கொள்ள வேண்டும் | No | — |
| TA-03 | என் ஆதார் எண் 1234 5678 9012 | Yes | Aadhaar-like |
| TA-04 | தயவுசெய்து 9876543210 எண்ணுக்கு அழையுங்கள் | Yes | Phone number |
| TA-05 | என் பெயர் கார்த்திக், நான் சென்னையில் இருக்கிறேன் | No | — |
| TA-06 | என் வங்கி கணக்கு எண் 112233445566 | Yes | Bank account |
| TA-07 | அலுவலகம் எத்தனை மணிக்கு திறக்கும்? | No | — |
| TA-08 | என் மின்னஞ்சல் karthik.demo@example.com | Yes | Email |
| TA-09 | வாடிக்கையாளர் சேவை நேரம் என்ன? | No | — |
| TA-10 | என் PAN கார்டு தொலைந்துவிட்டது, புதியது எப்படி பெறுவது | Yes | PAN |

## Telugu (10 examples)
| ID | Text | Sensitive? | Entity type |
|----|------|------------|-------------|
| TE-01 | నా PAN number ABCDE1234F | Yes | PAN |
| TE-02 | నా లోన్ స్టేటస్ ఏమిటి? | No | — |
| TE-03 | నా ఆధార్ నంబర్ 1234 5678 9012 | Yes | Aadhaar-like |
| TE-04 | దయచేసి 9876543210కి కాల్ చేయండి | Yes | Phone number |
| TE-05 | నా పేరు వెంకటేష్, నేను హైదరాబాద్‌లో ఉంటాను | No | — |
| TE-06 | నా బ్యాంక్ ఖాతా నంబర్ 112233445566 | Yes | Bank account |
| TE-07 | రేపు సెలవు ఉందా? | No | — |
| TE-08 | నా ఇమెయిల్ venkatesh.demo@example.com | Yes | Email |
| TE-09 | కస్టమర్ సర్వీస్ టైమింగ్స్ ఏమిటి? | No | — |
| TE-10 | నా PAN కార్డు పోయింది, కొత్తది ఎలా పొందాలి | Yes | PAN |

## Hinglish / Code-mixed (10 examples)
| ID | Text | Sensitive? | Entity type |
|----|------|------------|-------------|
| HG-01 | bro mera PAN ABCDE1234F hai, ispe check kardo | Yes | PAN |
| HG-02 | sir mera order kab aayega | No | — |
| HG-03 | mera account number 123456789012 hai, verify kardo | Yes | Bank account |
| HG-04 | yaar tumne meeting reschedule kyu ki | No | — |
| HG-05 | mera Aadhaar 1234 5678 9012 hai, isse link karo | Yes | Aadhaar-like |
| HG-06 | mujhe 9876543210 pe call kar dena | Yes | Phone number |
| HG-07 | is weekend movie chalte hai kya | No | — |
| HG-08 | mera email id rahul.demo@example.com hai, ispe bhejo | Yes | Email |
| HG-09 | office ka timing kya hai bhai | No | — |
| HG-10 | meri PAN card details ABCDE1234F leke KYC complete kardo | Yes | PAN |

---

## Corpus Summary
- 5 languages × 10 examples = **50 total test sentences**
- Roughly 60% sensitive / 40% safe per language — closer to a real support-chat distribution
  than a strict 50/50 split
- Entity types covered: PAN, Aadhaar-like number, phone number, bank account number, email

## TODO (stretch goal — later in the semester, not urgent for Day 2/3)
- [ ] Add adversarial/tricky cases: numbers split across two messages, deliberately
      obfuscated PAN ("A B C D E 1 2 3 4 F"), transliteration variants.
- [ ] Add multi-entity sentences (more than one sensitive item in one message).
- [ ] Expand to 20+ per language if early detection-engine results justify a bigger set.
