-- Extra visitor detail for the `visits` table.
-- Run once in the Supabase SQL editor (Dashboard → SQL → New query → Run).
-- Every column is nullable, so existing rows and the old site keep working;
-- old-site visits simply leave the new columns empty.
-- Safe to run more than once.

alter table public.visits add column if not exists city                text;
alter table public.visits add column if not exists region              text;
alter table public.visits add column if not exists country             text;
alter table public.visits add column if not exists isp                 text;
alter table public.visits add column if not exists utm_source          text;
alter table public.visits add column if not exists utm_medium          text;
alter table public.visits add column if not exists utm_campaign        text;
alter table public.visits add column if not exists scroll_depth        int;
alter table public.visits add column if not exists reached_form        boolean;
alter table public.visits add column if not exists viewed_testimonials boolean;
alter table public.visits add column if not exists returning_visitor   boolean;
alter table public.visits add column if not exists browser             text;
alter table public.visits add column if not exists os                  text;
alter table public.visits add column if not exists screen_size         text;
