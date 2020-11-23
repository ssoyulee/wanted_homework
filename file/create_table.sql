CREATE TABLE public.company
(
    company_id integer NOT NULL,
    company_rep_name text COLLATE pg_catalog."default",
    CONSTRAINT company_pkey PRIMARY KEY (company_id)
);

CREATE TABLE public.company_lang
(
    company_id integer NOT NULL,
    company_lang_type text COLLATE pg_catalog."default" NOT NULL,
    company_lang_name text COLLATE pg_catalog."default" NOT NULL,
    company_lang_tag text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT company_dtl_pkey PRIMARY KEY (company_id, company_lang_type)
);
