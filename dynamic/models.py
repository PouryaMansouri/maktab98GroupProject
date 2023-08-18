#django imports
from django.db import models
from django.utils.html import mark_safe

#inner modules imports
from utils import item_directory_path


# Create your models here.
class Footer(models.Model):
    footer_name = models.CharField(max_length=16)
    footer_phone = models.CharField(max_length=16)
    footer_logo = models.ImageField(upload_to='footer_logo/')
    footer_email = models.CharField(max_length=16)
    footer_text = models.CharField(max_length=255)
    footer_youtube = models.CharField(max_length=128,default='#')
    footer_telegram = models.CharField(max_length=128,default='#')
    footer_instagram = models.CharField(max_length=128,default='#')
    footer_googleplus = models.CharField(max_length=128,default='#')
    footer_twitter = models.CharField(max_length=128,default='#')

    def logo_preview(self): 
        return mark_safe(f'<img src = "{self.footer_logo.url}" width = "30"/>')

    def __str__(self) -> str:
        return str(self.footer_name)

class PageData(models.Model):

    target_name = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    route = models.CharField(max_length=64)
    banner = models.ImageField(upload_to=item_directory_path)
    footer = models.ForeignKey(Footer, on_delete= models.PROTECT)

    def banner_preview(self): 
        return mark_safe(f'<img src = "{self.banner.url}" width = "30"/>')
    
    def __str__(self) -> str:
        return str(self.target_name) + ' page data'

    @classmethod
    def get_page_date(cls, target):
        try:
            page_data = cls.objects.get(target_name = target)
            return page_data
        except:
            try:
                page_data = cls.objects.get(target_name = 'Default_Page')
                return page_data
            except:
                default_footer = Footer.objects.create(
                    footer_name = 'default',
                    footer_phone = '+989123456789',
                    footer_logo = 'footer_logo/logo.png',
                    footer_email = 'mail@mail.com',
                    footer_text = 'default text',
                )

                
                page_data = cls.objects.create(
                    target_name = 'Default_Page',
                    title = 'Cafena',
                    name = 'Cafena',
                    route = 'Default',
                    banner = 'PageData/banner.png',
                    footer = default_footer
                )

                return page_data