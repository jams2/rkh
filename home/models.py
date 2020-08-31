import re

from django.forms.utils import ErrorList
from django.core.validators import ValidationError
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock


TITLE_BLACKLIST_WORDS = ("the",)


class HomePage(Page):
    pass


class ImageGalleryBlock(blocks.StreamBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)


class LinkButtonValue(blocks.StructValue):
    def url(self):
        external = self.get("external_url")
        page = self.get("page")
        return external if external else page


class LinkButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    page = blocks.PageChooserBlock(required=False)
    external_url = blocks.URLBlock(required=False)

    def clean(self, value):
        errors = {}
        error_message = "choose either page or external_url"
        if (not value.get("page") and not value.get("external_url")) or (
            value.get("page") and value.get("external_url")
        ):
            errors["page"] = ErrorList([error_message])
            errors["external_url"] = ErrorList([error_message])
        if errors:
            raise ValidationError("Validation error in LinkButtonBlock", params=errors)
        return super().clean(value)

    class Meta:
        value_class = LinkButtonValue


def title_field_validator(val: str) -> None:
    for word in TITLE_BLACKLIST_WORDS:
        if word.lower() in val.lower():
            raise ValidationError('title cannot contain the word "the"')


def trim_punct(word: str) -> str:
    """Trim leading and trailing punctuation marks.
    """
    if len(word) < 2:
        return word if word[0].isalnum() else ""
    elif not word:
        return ""
    if not word[0].isalnum():
        word = word[1:]
    if not word[-1].isalnum():
        word = word[:-1]
    return word


class RKHStructBlock(blocks.StructBlock):
    title = blocks.CharBlock(validators=(title_field_validator,))
    content = blocks.RichTextBlock(features=["ol", "bold"])
    link_1 = LinkButtonBlock()
    link_2 = LinkButtonBlock()

    def clean(self, value):
        """Don't allow any word in the title to appear in the content.

        To get the blacklist from the title, split on whitespace. Trim
        leading and trailing punctuation so 'this.' or '"this' in the title
        will match 'this' in the content.

        Then do a case insensitive re.search to determine if any word
        in the title appears in the content. Add an error and bail out
        on the first match.
        """
        word_boundary = r"(\b|[^A-Z0-9])"  # word boundary or punctuation marks.
        errors = {}
        title_words = value.get("title").split()
        exclude_words = set(filter(lambda x: x, (trim_punct(x) for x in title_words)))
        content = value.get("content").source
        for word in exclude_words:
            pattern = word_boundary + word + word_boundary
            if re.search(pattern, content, re.IGNORECASE):
                errors["content"] = ErrorList(
                    [f'the word "{word}" cannot be in title AND content']
                )
                break
        if errors:
            raise ValidationError(
                "Words in title must not be in content", params=errors
            )
        return super().clean(value)


class FancyPage(Page):
    body = StreamField(
        [
            ("main_content", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("sub_section", RKHStructBlock()),
            ("image_gallery", ImageGalleryBlock(max_num=16)),
        ]
    )

    content_panels = Page.content_panels + [StreamFieldPanel("body")]
