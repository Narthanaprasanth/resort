from django.db import models

class Agent(models.Model):
    # Step 0: Agency Details
    agency_name = models.CharField(max_length=255)
    year_established = models.CharField(max_length=10)
    website = models.URLField(blank=True, null=True)
    company_type = models.CharField(max_length=50)
    primary_market = models.CharField(max_length=50)

    # Step 1: Contact + Address
    contact_name = models.CharField(max_length=255)
    contact_designation = models.CharField(max_length=100)
    contact_mobile = models.CharField(max_length=50)
    contact_email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    pin = models.CharField(max_length=20, blank=True, null=True)

    # Step 2: Business Profile
    top_destinations = models.CharField(max_length=255)
    avg_monthly_bookings = models.CharField(max_length=100)
    client_types = models.JSONField(default=list)

    # Step 3: Partnership Expectations
    expected_monthly_room_nights = models.CharField(max_length=100)
    preferred_room_category = models.CharField(max_length=100, blank=True, null=True)
    commission_requested = models.CharField(max_length=50)
    preferred_payment_terms = models.CharField(max_length=100)

    # Step 4: Banking Details
    bank_name = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=50)
    
    docs_gst = models.FileField(upload_to='agent_docs/', blank=True, null=True)
    docs_pan = models.FileField(upload_to='agent_docs/', blank=True, null=True)
    docs_company = models.FileField(upload_to='agent_docs/', blank=True, null=True)
    docs_cheque = models.FileField(upload_to='agent_docs/', blank=True, null=True)

    # Step 5: Terms + Declaration
    agreed = models.BooleanField(default=False)
    signatory_name = models.CharField(max_length=255)
    signatory_designation = models.CharField(max_length=100)
    signatory_date = models.DateField(blank=True, null=True)

    # Office Use
    status = models.CharField(max_length=50, default='Pending')
    vendor_id = models.CharField(max_length=50, blank=True, null=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    date_of_approval = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agency_name

class SiteConfiguration(models.Model):
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    header_bg_color = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default='#0f2418',
        help_text='Header background color (e.g. #0f2418 or any CSS color)'
    )

    def __str__(self):
        return "Site Configuration"
    
    def save(self, *args, **kwargs):
        # Implement singleton pattern — always reuse pk=1
        if not self.pk and SiteConfiguration.objects.exists():
            self.pk = SiteConfiguration.objects.first().pk
        super().save(*args, **kwargs)
