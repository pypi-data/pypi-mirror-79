# django-balloon-block-editor

## Installation

- `pip install django-balloon-block-editor`
- In `settings.py`, add `balloon_block_editor` to `INSTALLED_APPS`

## Usage

In `models.py`:

```
from balloon_block_editor.fields import BalloonBlockField
from django.db import models


class Test(models.Model):
    content = BalloonBlockField()
```

