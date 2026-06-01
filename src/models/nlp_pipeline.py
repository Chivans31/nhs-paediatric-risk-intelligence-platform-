# NLP PIPELINE

from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis"
)

clinical_note = "Patient showing severe complications and unstable glucose levels"

result = classifier(clinical_note)

print(result)