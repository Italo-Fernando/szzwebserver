CREATE TYPE req_status as ENUM ('WAITING', 'PROCESSING', 'FINISHED', 'ERROR');

CREATE TABLE public.execution_result (
    bugfix_commit_hash text NOT NULL,
    repository_url text NOT NULL,
    szz_variant text NOT NULL,
    bug_commit_hashes text[],
    request_status req_status NOT NULL
);

CREATE TABLE public.request (
    request_id bigint NOT NULL,
    repository_url text NOT NULL,
    szz_variant text NOT NULL,
    bugfix_commit_hashes text[] NOT NULL,
    commit_count integer NOT NULL
);

CREATE SEQUENCE public.request_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.request_id_seq OWNED BY public.request.request_id;


CREATE TABLE public.request_status (
    request_id bigint NOT NULL,
    bugfix_commit_hash text NOT NULL,
    finished boolean DEFAULT false NOT NULL
);

CREATE TABLE public.szz_variant (
    id integer NOT NULL,
    variant_name character varying(20)
);

ALTER TABLE ONLY public.request ALTER COLUMN request_id SET DEFAULT nextval('public.request_id_seq'::regclass);

-- ################ User permissions #################


ALTER TABLE public.execution_result OWNER TO example;
ALTER TABLE public.request OWNER TO example;
ALTER SEQUENCE public.request_id_seq OWNER TO example;
ALTER TABLE public.request_status OWNER TO example;
ALTER TABLE public.szz_variant OWNER TO example;

-- ################ User permissions End #################


ALTER TABLE ONLY public.szz_variant
    ADD CONSTRAINT szz_variant_pkey PRIMARY KEY (id);

GRANT ALL ON SCHEMA public TO example;
