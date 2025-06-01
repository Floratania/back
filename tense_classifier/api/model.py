import torch.nn as nn
from transformers import BertModel

tense_labels = {
    'Future Continuous': 0, 'Future Perfect': 1, 'Future Perfect Continuous': 2, 'Future Simple': 3,
    'Past Continuous': 4, 'Past Perfect': 5, 'Past Perfect Continuous': 6, 'Past Simple': 7,
    'Present Continuous': 8, 'Present Perfect': 9, 'Present Perfect Continuous': 10, 'Present Simple': 11
}

class TenseClassifier(nn.Module):
    def __init__(self, num_classes=12):
        super().__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.fc = nn.Sequential(
            nn.ReLU(),
            nn.Linear(self.bert.config.hidden_size, num_classes)
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        return self.fc(outputs.last_hidden_state[:, 0, :])


