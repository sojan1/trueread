--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    displayname character varying,
    email character varying,
    password character varying,
    name character varying,
    phone character varying,
    did character varying,
    didverified boolean,
    status character varying(9)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, displayname, email, password, name, phone, did, didverified, status) FROM stdin;
2a32007c-4612-43fd-9d26-957581b2fd86	Sojan	sojan@gmail.com	$2b$12$h8PkY7ywteeB0O4HxtAwa.HoaMnvbZAq/to/GZK3hoIWFd.lfs99y	Sojan Chandy 	123456	\N	f	ACTIVE
\.


--
-- Name: users users_did_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_did_key UNIQUE (did);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_users_displayname; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_displayname ON public.users USING btree (displayname);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- PostgreSQL database dump complete
--

