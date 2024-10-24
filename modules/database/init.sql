CREATE TYPE req_status as ENUM ('WAITING', 'PROCESSING', 'FINISHED', 'ERROR');

CREATE TABLE public.szz_variant (
    variant_name character varying(20),
    PRIMARY KEY (variant_name)
);

CREATE TABLE public.execution_result (
    bugfix_commit_hash text NOT NULL,
    repository_url text NOT NULL,
    szz_variant text REFERENCES szz_variant NOT NULL,
    bug_commit_hashes text[],
    PRIMARY KEY (repository_url, bugfix_commit_hash, szz_variant)
);

CREATE TABLE public.request (
    request_id bigint PRIMARY KEY,
    repository_url text NOT NULL,
    szz_variant text REFERENCES szz_variant NOT NULL,
    bugfix_commit_hashes text[] NOT NULL,
    request_status req_status NOT NULL DEFAULT 'WAITING',
    retry_count integer NOT NULL DEFAULT 0,
    info text
);

CREATE SEQUENCE public.request_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.request_id_seq OWNED BY public.request.request_id;


CREATE TABLE public.commit_to_request_link (
    request_id bigint REFERENCES request ON DELETE CASCADE NOT NULL,
    bugfix_commit_hash text NOT NULL,
    repository_url text NOT NULL,
    szz_variant text REFERENCES szz_variant NOT NULL,
    request_status req_status NOT NULL DEFAULT 'WAITING'
);

ALTER TABLE ONLY public.request ALTER COLUMN request_id SET DEFAULT nextval('public.request_id_seq'::regclass);

-- ################ User permissions #################


ALTER TABLE public.execution_result OWNER TO example;
ALTER TABLE public.request OWNER TO example;
ALTER SEQUENCE public.request_id_seq OWNER TO example;
ALTER TABLE public.commit_to_request_link OWNER TO example;
ALTER TABLE public.szz_variant OWNER TO example;

-- ################ User permissions End #################

GRANT ALL ON SCHEMA public TO example;
