from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **options):
        # Создаем группу
        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" создана')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Модератор продуктов" уже существует')
            )

        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем права
        permissions = []

        # 1. Право на отмену публикации
        unpublish_perm, _ = Permission.objects.get_or_create(
            codename="can_unpublish_product",
            name="Может отменять публикацию продукта",
            content_type=content_type,
        )
        permissions.append(unpublish_perm)

        # 2. Право на удаление любого продукта
        delete_perm = Permission.objects.get(
            codename="delete_product", content_type=content_type
        )
        permissions.append(delete_perm)

        # Назначаем права группе
        group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Назначены права группе:"))
        self.stdout.write("  - can_unpublish_product (отмена публикации)")
        self.stdout.write("  - delete_product (удаление продукта)")

        self.stdout.write(self.style.SUCCESS("\n✅ Готово!"))
