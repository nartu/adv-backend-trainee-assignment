--
-- PostgreSQL database dump
--

-- Dumped from database version 12.6 (Ubuntu 12.6-0ubuntu0.20.10.1)
-- Dumped by pg_dump version 12.6 (Ubuntu 12.6-0ubuntu0.20.10.1)

-- Started on 2021-02-25 21:11:55 MSK

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

--
-- TOC entry 2 (class 3079 OID 16743)
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 3011 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 203 (class 1259 OID 16740)
-- Name: ads_main; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ads_main (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    name character varying(200) NOT NULL,
    description character varying(1000) NOT NULL,
    price numeric(20,2) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.ads_main OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16794)
-- Name: ads_photo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ads_photo (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    main_id uuid NOT NULL,
    photo_url character varying(255) NOT NULL
);


ALTER TABLE public.ads_photo OWNER TO postgres;

--
-- TOC entry 2876 (class 2606 OID 16783)
-- Name: ads_main ads_main_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ads_main
    ADD CONSTRAINT ads_main_pkey PRIMARY KEY (id);


--
-- TOC entry 2878 (class 2606 OID 16799)
-- Name: ads_photo ads_photo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ads_photo
    ADD CONSTRAINT ads_photo_pkey PRIMARY KEY (id);


--
-- TOC entry 2879 (class 2606 OID 16802)
-- Name: ads_photo ads_photo_main_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ads_photo
    ADD CONSTRAINT ads_photo_main_id_fkey FOREIGN KEY (main_id) REFERENCES public.ads_main(id);


-- Completed on 2021-02-25 21:11:57 MSK

--
-- PostgreSQL database dump complete
--
