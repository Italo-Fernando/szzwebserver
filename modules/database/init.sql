--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Ubuntu 16.2-1.pgdg20.04+1)
-- Dumped by pg_dump version 16.2 (Ubuntu 16.2-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bug_to_fix; Type: TABLE; Schema: public; Owner: example
--

CREATE TABLE public.bug_to_fix (
    bugfix_commit_hash text NOT NULL,
    repository_url text NOT NULL,
    szz_variant text NOT NULL,
    bug_commit_hashes text[]
);


ALTER TABLE public.bug_to_fix OWNER TO example;

--
-- Name: mytable; Type: TABLE; Schema: public; Owner: rockett
--

CREATE TABLE public.mytable (
    id integer
);


ALTER TABLE public.mytable OWNER TO rockett;

--
-- Name: repository; Type: TABLE; Schema: public; Owner: example
--

CREATE TABLE public.repository (
    id uuid NOT NULL,
    url text NOT NULL,
    status character varying(15)
);


ALTER TABLE public.repository OWNER TO example;

--
-- Name: request; Type: TABLE; Schema: public; Owner: example
--

CREATE TABLE public.request (
    request_id bigint NOT NULL,
    repository_url text NOT NULL,
    szz_variant text NOT NULL,
    bugfix_commit_hashes text[] NOT NULL,
    commit_count integer NOT NULL
);


ALTER TABLE public.request OWNER TO example;

--
-- Name: request_id_seq; Type: SEQUENCE; Schema: public; Owner: example
--

CREATE SEQUENCE public.request_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.request_id_seq OWNER TO example;

--
-- Name: request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: example
--

ALTER SEQUENCE public.request_id_seq OWNED BY public.request.request_id;


--
-- Name: request_status; Type: TABLE; Schema: public; Owner: example
--

CREATE TABLE public.request_status (
    request_id bigint NOT NULL,
    bugfix_commit_hash text NOT NULL,
    finished boolean DEFAULT false NOT NULL
);


ALTER TABLE public.request_status OWNER TO example;

--
-- Name: szz_variant; Type: TABLE; Schema: public; Owner: example
--

CREATE TABLE public.szz_variant (
    id integer NOT NULL,
    variant_name character varying(20)
);


ALTER TABLE public.szz_variant OWNER TO example;

--
-- Name: request request_id; Type: DEFAULT; Schema: public; Owner: example
--

ALTER TABLE ONLY public.request ALTER COLUMN request_id SET DEFAULT nextval('public.request_id_seq'::regclass);


--
-- Data for Name: bug_to_fix; Type: TABLE DATA; Schema: public; Owner: example
--

COPY public.bug_to_fix (bugfix_commit_hash, repository_url, szz_variant, bug_commit_hashes) FROM stdin;
588ce9b1dade5e7db703fb9af603184a09ae4494	https://github.com/gpac/gpac	R_SZZ	{50d526f7071debbaf9b3e8f5fdddc905a4ed4d55}
3faf12cd8603e3efbcc7e570e07dfd1ea2a17095	https://github.com/torvalds/linux	R_SZZ	{7056d423f16103f6700569f60ca842d91bfaabab}
8b16295318cd85c55b04e962479de1c6532a6759	https://github.com/SimpleServer/SimpleServer	R_SZZ	{2f38776480ff18555f3bd2cf89d566bef8047916}
\.


--
-- Data for Name: mytable; Type: TABLE DATA; Schema: public; Owner: rockett
--

COPY public.mytable (id) FROM stdin;
\.


--
-- Data for Name: repository; Type: TABLE DATA; Schema: public; Owner: example
--

COPY public.repository (id, url, status) FROM stdin;
\.


--
-- Data for Name: request; Type: TABLE DATA; Schema: public; Owner: example
--

COPY public.request (request_id, repository_url, szz_variant, bugfix_commit_hashes, commit_count) FROM stdin;
64	https://github.com/DemocracyClub/yournextrepresentative	R_SZZ	{0722309a9c242aac28d2cb33798abbd18b233aa0}	1
65	https://github.com/DemocracyClub/yournextrepresentative	R_SZZ	{0722309a9c242aac28d2cb33798abbd18b233aa0}	1
66	https://github.com/DemocracyClub/yournextrepresentative	R_SZZ	{0722309a9c242aac28d2cb33798abbd18b233aa0}	1
67	https://github.com/DemocracyClub/yournextrepresentative	R_SZZ	{0722309a9c242aac28d2cb33798abbd18b233aa0}	1
68	https://github.com/DemocracyClub/yournextrepresentative	R_SZZ	{0722309a9c242aac28d2cb33798abbd18b233aa0}	1
69	https://github.com/DemocracyClub/yournextrepresentative	R_SZZ	{0722309a9c242aac28d2cb33798abbd18b233aa0}	1
70	https://github.com/ahobson/ruby-pcap	R_SZZ	{0ad41d0684c2ec4c2a6b604f7aafbaf9f0459dcc}	1
71	https://github.com/HachasyDados/HD-TCore	R_SZZ	{319ecd792dad03dccfd1dbfa64b3be593ff46b1b}	1
72	https://github.com/HachasyDados/HD-TCore	R_SZZ	{319ecd792dad03dccfd1dbfa64b3be593ff46b1b}	1
73	https://github.com/HachasyDados/HD-TCore	R_SZZ	{319ecd792dad03dccfd1dbfa64b3be593ff46b1b}	1
74	https://github.com/HachasyDados/HD-TCore	R_SZZ	{319ecd792dad03dccfd1dbfa64b3be593ff46b1b}	1
75	https://github.com/gpac/gpac	R_SZZ	{588ce9b1dade5e7db703fb9af603184a09ae4494}	1
76	https://github.com/gpac/gpac	R_SZZ	{588ce9b1dade5e7db703fb9af603184a09ae4494}	1
77	https://github.com/gpac/gpac	R_SZZ	{588ce9b1dade5e7db703fb9af603184a09ae4494}	1
78	https://github.com/torvalds/linux	R_SZZ	{3faf12cd8603e3efbcc7e570e07dfd1ea2a17095}	1
79	https://github.com/torvalds/linux	R_SZZ	{3faf12cd8603e3efbcc7e570e07dfd1ea2a17095}	1
80	https://github.com/torvalds/linux	R_SZZ	{3faf12cd8603e3efbcc7e570e07dfd1ea2a17095}	1
81	https://github.com/SimpleServer/SimpleServer	R_SZZ	{8b16295318cd85c55b04e962479de1c6532a6759}	1
\.


--
-- Data for Name: request_status; Type: TABLE DATA; Schema: public; Owner: example
--

COPY public.request_status (request_id, bugfix_commit_hash, finished) FROM stdin;
77	588ce9b1dade5e7db703fb9af603184a09ae4494	t
78	3faf12cd8603e3efbcc7e570e07dfd1ea2a17095	f
79	3faf12cd8603e3efbcc7e570e07dfd1ea2a17095	t
80	3faf12cd8603e3efbcc7e570e07dfd1ea2a17095	t
81	8b16295318cd85c55b04e962479de1c6532a6759	t
64	0722309a9c242aac28d2cb33798abbd18b233aa0	t
65	0722309a9c242aac28d2cb33798abbd18b233aa0	t
66	0722309a9c242aac28d2cb33798abbd18b233aa0	t
67	0722309a9c242aac28d2cb33798abbd18b233aa0	t
68	0722309a9c242aac28d2cb33798abbd18b233aa0	t
69	0722309a9c242aac28d2cb33798abbd18b233aa0	t
70	0ad41d0684c2ec4c2a6b604f7aafbaf9f0459dcc	t
71	319ecd792dad03dccfd1dbfa64b3be593ff46b1b	t
72	319ecd792dad03dccfd1dbfa64b3be593ff46b1b	t
73	319ecd792dad03dccfd1dbfa64b3be593ff46b1b	t
74	319ecd792dad03dccfd1dbfa64b3be593ff46b1b	t
75	588ce9b1dade5e7db703fb9af603184a09ae4494	t
76	588ce9b1dade5e7db703fb9af603184a09ae4494	t
\.


--
-- Data for Name: szz_variant; Type: TABLE DATA; Schema: public; Owner: example
--

COPY public.szz_variant (id, variant_name) FROM stdin;
1	B_SZZ
2	R_SZZ
\.


--
-- Name: request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: example
--

SELECT pg_catalog.setval('public.request_id_seq', 81, true);


--
-- Name: repository repository_pkey; Type: CONSTRAINT; Schema: public; Owner: example
--

ALTER TABLE ONLY public.repository
    ADD CONSTRAINT repository_pkey PRIMARY KEY (id);


--
-- Name: szz_variant szz_variant_pkey; Type: CONSTRAINT; Schema: public; Owner: example
--

ALTER TABLE ONLY public.szz_variant
    ADD CONSTRAINT szz_variant_pkey PRIMARY KEY (id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO example;
GRANT ALL ON SCHEMA public TO rockett;


--
-- PostgreSQL database dump complete
--

