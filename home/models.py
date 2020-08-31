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


def trim_trailing_punct(word: str) -> str:
    return word if word[-1].isalnum() else word[:-1]


class RKHStructBlock(blocks.StructBlock):
    title = blocks.CharBlock(validators=(title_field_validator,))
    content = blocks.RichTextBlock(features=["ol", "bold"])
    link_1 = LinkButtonBlock()
    link_2 = LinkButtonBlock()

    def clean(self, value):
        errors = {}
        exclude_words = set(
            trim_trailing_punct(x.lower()) for x in value.get("title").split()
        )
        content = value.get("content").source.lower()
        for word in exclude_words:
            if word in content:
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
