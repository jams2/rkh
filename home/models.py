from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    pass


class LinkButtonValue(blocks.StructValue):
    def url(self):
        external = self.get("external_url")
        page = self.get("page")
        return external if external else page


class LinkButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    page = blocks.PageChooserBlock(required=False)
    external_url = blocks.URLBlock(required=False)

    class Meta:
        value_class = LinkButtonValue


class RKHStructBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock()
    link_1 = LinkButtonBlock(required=True)
    link_2 = LinkButtonBlock(required=True)


class FancyPage(Page):
    body = StreamField(
        [
            ("main_content", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("sub_section", RKHStructBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]
