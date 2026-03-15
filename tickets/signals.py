from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Ticket, TicketActivity
from .services import auto_assign_ticket

@receiver(post_save, sender=Ticket)
def handle_ticket_created(sender, instance, created, **kwargs):

    if created:

        # Log ticket creation
        TicketActivity.objects.create(
            ticket=instance,
            message="Ticket created."
        )

        # Assign agent automatically
        if not instance.assigned_to:
            auto_assign_ticket(instance)

@receiver(pre_save, sender=Ticket)
def log_ticket_status_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_ticket = Ticket.objects.get(pk=instance.pk)
            
            # Log Status Changes
            if old_ticket.status != instance.status:
                TicketActivity.objects.create(
                    ticket=instance,
                    message=f"Status changed from {old_ticket.status} to {instance.status}."
                )
            
            # Log Assignment Changes
            if old_ticket.assigned_to != instance.assigned_to:
                if instance.assigned_to:
                    TicketActivity.objects.create(
                        ticket=instance,
                        message=f"Ticket assigned to {instance.assigned_to.username}."
                    )
                else:
                    TicketActivity.objects.create(
                        ticket=instance,
                        message="Ticket unassigned."
                    )
                    
        except Ticket.DoesNotExist:
            pass