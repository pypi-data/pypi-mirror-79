# django-balloon-block-field

## Installation

- `pip install django-balloon-block-field`
- In `settings.py`, add `balloon_block_field` to `INSTALLED_APPS`

## Usage

In `models.py`:

```
from balloon_block_field.fields import BalloonBlockField
from django.db import models


class Test(models.Model):
    content = BalloonBlockField()
```


