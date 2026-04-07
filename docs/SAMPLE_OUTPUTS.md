# Sample Outputs

Use these snippets in listings, outreach, or handoff notes when you want to show what the repository produces without running a live demo.

## Training Output

```text
✅ Data loaded successfully with shape: (2205, 39)
✅ Data split into training and test sets. Training size: (1764, 38), Test size: (441, 38)
✅ Initialized LogisticRegression model with params: {'max_iter': 1000}
✅ Model training completed.
Test Accuracy: 0.8730
Test Precision: 0.8651
Test Recall: 0.8730
Test F1 Score: 0.8678
✅ Trained model saved successfully at: models/artifacts/models/trained_model_20260407_130000.pkl
✅ Evaluation metrics saved successfully at: models/artifacts/models/trained_model_20260407_130000_metrics.json
```

## Evaluation Output

```text
Model Evaluation Metrics:
Accuracy: 0.8730
Precision: 0.8651
Recall: 0.8730
F1 Score: 0.8678

Evaluation metrics saved to models/outputs/trained_model_20260407_130000_evaluation.json
```

## FastAPI Output

```json
{"status":"ok"}
```

```json
[
  {"customer_id":1,"Income":58000,"Recency":10},
  {"customer_id":2,"Income":42000,"Recency":24}
]
```

## GenAI Brief Output

```json
{
  "campaign_summary": "CampaignForge AI should position CampaignForge AI for agencies, freelancers, and startup marketing teams using reusable messaging angles and prompt-ready creative direction.",
  "channel_recommendations": ["LinkedIn", "Email", "Landing Page"],
  "tone_options": ["Confident", "Practical", "Forward-Looking"]
}
```

```text
Angle: Outcome-Driven Launch
- 5 headline variants
- 3 body copy variants
- 3 CTA variants
- 3 image prompts for the next generation stage
```

## CRM Dry-Run Message

```text
Dry run complete: prepared 20 records for Salesforce.
Endpoint: https://example.my.salesforce.com/services/data/v60.0/composite/tree/Lead
```

## Listing-Friendly Summary

```text
Includes ETL, model training, evaluation, FastAPI service, Streamlit dashboard,
GenAI brief generation, Airflow DAGs, Docker assets, Kubernetes manifests, and CI workflows in one repository.
```
