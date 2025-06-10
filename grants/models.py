# -*- coding: utf-8 -*-
from django.db import models


class Grant(models.Model):
    site = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    grantor = models.TextField(blank=True, null=True)
    facts = models.TextField(blank=True, null=True)
    deadline = models.TextField(blank=True, null=True)
    amount = models.TextField(blank=True, null=True)
    application_url = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def get_countries_list(self):
        return [c.strip() for c in self.country.split(',') if c.strip()]

    def get_facts_list(self):
        if not self.facts:
            return []
        return [fact.strip() for fact in self.facts.split('•') if fact.strip()]

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'grants' 