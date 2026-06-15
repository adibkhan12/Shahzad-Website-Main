--
-- PostgreSQL database dump
--

-- Dumped from database version 16.6
-- Dumped by pg_dump version 16.6

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

ALTER TABLE IF EXISTS ONLY public.wishlist_wishedproduct DROP CONSTRAINT IF EXISTS wishlist_wishedproduct_user_id_1f294dea_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.wishlist_wishedproduct DROP CONSTRAINT IF EXISTS wishlist_wishedprodu_product_id_4fbea32e_fk_catalog_p;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialaccount DROP CONSTRAINT IF EXISTS socialaccount_social_user_id_8146e70c_fk_accounts_;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialapp_sites DROP CONSTRAINT IF EXISTS socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialapp_sites DROP CONSTRAINT IF EXISTS socialaccount_social_site_id_2579dee5_fk_django_si;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialtoken DROP CONSTRAINT IF EXISTS socialaccount_social_app_id_636a42d7_fk_socialacc;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialtoken DROP CONSTRAINT IF EXISTS socialaccount_social_account_id_951f210e_fk_socialacc;
ALTER TABLE IF EXISTS ONLY public.repairs_repairbooking DROP CONSTRAINT IF EXISTS repairs_repairbookin_service_id_65466e21_fk_repairs_r;
ALTER TABLE IF EXISTS ONLY public.orders_orderitem DROP CONSTRAINT IF EXISTS orders_orderitem_product_id_afe4254a_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.orders_orderitem DROP CONSTRAINT IF EXISTS orders_orderitem_order_id_fe61a34d_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.orders_order DROP CONSTRAINT IF EXISTS orders_order_user_id_e9b59eb1_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.catalog_stockmovement DROP CONSTRAINT IF EXISTS catalog_stockmovement_user_id_fb907961_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.catalog_stockmovement DROP CONSTRAINT IF EXISTS catalog_stockmovement_product_id_13308dcf_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.catalog_review DROP CONSTRAINT IF EXISTS catalog_review_product_id_e494243b_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.catalog_qa DROP CONSTRAINT IF EXISTS catalog_qa_product_id_2f5761a3_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.catalog_productimage DROP CONSTRAINT IF EXISTS catalog_productimage_product_id_1f42dd8c_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.catalog_product DROP CONSTRAINT IF EXISTS catalog_product_category_id_35bf920b_fk_catalog_category_id;
ALTER TABLE IF EXISTS ONLY public.catalog_product DROP CONSTRAINT IF EXISTS catalog_product_brand_id_bb0c7890_fk_catalog_brand_id;
ALTER TABLE IF EXISTS ONLY public.catalog_homepage DROP CONSTRAINT IF EXISTS catalog_homepage_hero_product_id_594e8ad1_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.catalog_category DROP CONSTRAINT IF EXISTS catalog_category_parent_id_f61bd017_fk_catalog_category_id;
ALTER TABLE IF EXISTS ONLY public.catalog_brand DROP CONSTRAINT IF EXISTS catalog_brand_category_id_9bf3af96_fk_catalog_category_id;
ALTER TABLE IF EXISTS ONLY public.cart_cartitem DROP CONSTRAINT IF EXISTS cart_cartitem_product_id_b24e265a_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.cart_cartitem DROP CONSTRAINT IF EXISTS cart_cartitem_cart_id_370ad265_fk_cart_cart_id;
ALTER TABLE IF EXISTS ONLY public.cart_cart DROP CONSTRAINT IF EXISTS cart_cart_user_id_9b4220b9_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.accounts_user_user_permissions DROP CONSTRAINT IF EXISTS accounts_user_user_p_user_id_e4f0a161_fk_accounts_;
ALTER TABLE IF EXISTS ONLY public.accounts_user_user_permissions DROP CONSTRAINT IF EXISTS accounts_user_user_p_permission_id_113bb443_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.accounts_user_groups DROP CONSTRAINT IF EXISTS accounts_user_groups_user_id_52b62117_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.accounts_user_groups DROP CONSTRAINT IF EXISTS accounts_user_groups_group_id_bd11a704_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.accounts_address DROP CONSTRAINT IF EXISTS accounts_address_user_id_c8c74ddf_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.account_emailconfirmation DROP CONSTRAINT IF EXISTS account_emailconfirm_email_address_id_5b7f8c58_fk_account_e;
ALTER TABLE IF EXISTS ONLY public.account_emailaddress DROP CONSTRAINT IF EXISTS account_emailaddress_user_id_2c513194_fk_accounts_user_id;
DROP INDEX IF EXISTS public.wishlist_wishedproduct_user_id_1f294dea;
DROP INDEX IF EXISTS public.wishlist_wishedproduct_product_id_4fbea32e;
DROP INDEX IF EXISTS public.unique_verified_email;
DROP INDEX IF EXISTS public.unique_primary_email;
DROP INDEX IF EXISTS public.socialaccount_socialtoken_app_id_636a42d7;
DROP INDEX IF EXISTS public.socialaccount_socialtoken_account_id_951f210e;
DROP INDEX IF EXISTS public.socialaccount_socialapp_sites_socialapp_id_97fb6e7d;
DROP INDEX IF EXISTS public.socialaccount_socialapp_sites_site_id_2579dee5;
DROP INDEX IF EXISTS public.socialaccount_socialaccount_user_id_8146e70c;
DROP INDEX IF EXISTS public.repairs_repairservice_slug_e3338d11_like;
DROP INDEX IF EXISTS public.repairs_repairbooking_service_id_65466e21;
DROP INDEX IF EXISTS public.orders_orderitem_product_id_afe4254a;
DROP INDEX IF EXISTS public.orders_orderitem_order_id_fe61a34d;
DROP INDEX IF EXISTS public.orders_order_user_id_e9b59eb1;
DROP INDEX IF EXISTS public.django_site_domain_a2e37b91_like;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.catalog_stockmovement_user_id_fb907961;
DROP INDEX IF EXISTS public.catalog_stockmovement_product_id_13308dcf;
DROP INDEX IF EXISTS public.catalog_setting_name_64ff6d39_like;
DROP INDEX IF EXISTS public.catalog_review_product_id_e494243b;
DROP INDEX IF EXISTS public.catalog_qa_product_id_2f5761a3;
DROP INDEX IF EXISTS public.catalog_productimage_product_id_1f42dd8c;
DROP INDEX IF EXISTS public.catalog_product_slug_f37848b0_like;
DROP INDEX IF EXISTS public.catalog_product_category_id_35bf920b;
DROP INDEX IF EXISTS public.catalog_product_brand_409aa74f;
DROP INDEX IF EXISTS public.catalog_pro_is_acti_14fc6b_idx;
DROP INDEX IF EXISTS public.catalog_homepage_hero_product_id_594e8ad1;
DROP INDEX IF EXISTS public.catalog_category_slug_dbf63ad0_like;
DROP INDEX IF EXISTS public.catalog_category_parent_id_f61bd017;
DROP INDEX IF EXISTS public.catalog_brand_slug_988c8dbc_like;
DROP INDEX IF EXISTS public.catalog_brand_category_id_9bf3af96;
DROP INDEX IF EXISTS public.cart_cartitem_product_id_b24e265a;
DROP INDEX IF EXISTS public.cart_cartitem_cart_id_370ad265;
DROP INDEX IF EXISTS public.cart_cart_session_key_bf21cb35_like;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
DROP INDEX IF EXISTS public.accounts_user_username_6088629e_like;
DROP INDEX IF EXISTS public.accounts_user_user_permissions_user_id_e4f0a161;
DROP INDEX IF EXISTS public.accounts_user_user_permissions_permission_id_113bb443;
DROP INDEX IF EXISTS public.accounts_user_groups_user_id_52b62117;
DROP INDEX IF EXISTS public.accounts_user_groups_group_id_bd11a704;
DROP INDEX IF EXISTS public.accounts_user_email_b2644a56_like;
DROP INDEX IF EXISTS public.accounts_address_user_id_c8c74ddf;
DROP INDEX IF EXISTS public.account_emailconfirmation_key_f43612bd_like;
DROP INDEX IF EXISTS public.account_emailconfirmation_email_address_id_5b7f8c58;
DROP INDEX IF EXISTS public.account_emailaddress_user_id_2c513194;
DROP INDEX IF EXISTS public.account_emailaddress_email_03be32b2_like;
DROP INDEX IF EXISTS public.account_emailaddress_email_03be32b2;
ALTER TABLE IF EXISTS ONLY public.wishlist_wishedproduct DROP CONSTRAINT IF EXISTS wishlist_wishedproduct_user_id_product_id_338094c4_uniq;
ALTER TABLE IF EXISTS ONLY public.wishlist_wishedproduct DROP CONSTRAINT IF EXISTS wishlist_wishedproduct_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_brand DROP CONSTRAINT IF EXISTS unique_brand_per_category;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialtoken DROP CONSTRAINT IF EXISTS socialaccount_socialtoken_pkey;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialtoken DROP CONSTRAINT IF EXISTS socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialapp_sites DROP CONSTRAINT IF EXISTS socialaccount_socialapp_sites_pkey;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialapp DROP CONSTRAINT IF EXISTS socialaccount_socialapp_pkey;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialapp_sites DROP CONSTRAINT IF EXISTS socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialaccount DROP CONSTRAINT IF EXISTS socialaccount_socialaccount_provider_uid_fc810c6e_uniq;
ALTER TABLE IF EXISTS ONLY public.socialaccount_socialaccount DROP CONSTRAINT IF EXISTS socialaccount_socialaccount_pkey;
ALTER TABLE IF EXISTS ONLY public.repairs_repairservice DROP CONSTRAINT IF EXISTS repairs_repairservice_slug_key;
ALTER TABLE IF EXISTS ONLY public.repairs_repairservice DROP CONSTRAINT IF EXISTS repairs_repairservice_pkey;
ALTER TABLE IF EXISTS ONLY public.repairs_repairbooking DROP CONSTRAINT IF EXISTS repairs_repairbooking_reference_key;
ALTER TABLE IF EXISTS ONLY public.repairs_repairbooking DROP CONSTRAINT IF EXISTS repairs_repairbooking_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_orderitem DROP CONSTRAINT IF EXISTS orders_orderitem_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_order DROP CONSTRAINT IF EXISTS orders_order_reference_key;
ALTER TABLE IF EXISTS ONLY public.orders_order DROP CONSTRAINT IF EXISTS orders_order_pkey;
ALTER TABLE IF EXISTS ONLY public.django_site DROP CONSTRAINT IF EXISTS django_site_pkey;
ALTER TABLE IF EXISTS ONLY public.django_site DROP CONSTRAINT IF EXISTS django_site_domain_a2e37b91_uniq;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_stockmovement DROP CONSTRAINT IF EXISTS catalog_stockmovement_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_setting DROP CONSTRAINT IF EXISTS catalog_setting_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_setting DROP CONSTRAINT IF EXISTS catalog_setting_name_key;
ALTER TABLE IF EXISTS ONLY public.catalog_review DROP CONSTRAINT IF EXISTS catalog_review_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_qa DROP CONSTRAINT IF EXISTS catalog_qa_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_productimage DROP CONSTRAINT IF EXISTS catalog_productimage_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_product DROP CONSTRAINT IF EXISTS catalog_product_slug_key;
ALTER TABLE IF EXISTS ONLY public.catalog_product DROP CONSTRAINT IF EXISTS catalog_product_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_homepage DROP CONSTRAINT IF EXISTS catalog_homepage_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_category DROP CONSTRAINT IF EXISTS catalog_category_slug_key;
ALTER TABLE IF EXISTS ONLY public.catalog_category DROP CONSTRAINT IF EXISTS catalog_category_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_brand DROP CONSTRAINT IF EXISTS catalog_brand_slug_key;
ALTER TABLE IF EXISTS ONLY public.catalog_brand DROP CONSTRAINT IF EXISTS catalog_brand_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_adbanner DROP CONSTRAINT IF EXISTS catalog_adbanner_pkey;
ALTER TABLE IF EXISTS ONLY public.cart_cartitem DROP CONSTRAINT IF EXISTS cart_cartitem_pkey;
ALTER TABLE IF EXISTS ONLY public.cart_cartitem DROP CONSTRAINT IF EXISTS cart_cartitem_cart_id_product_id_53cce7c3_uniq;
ALTER TABLE IF EXISTS ONLY public.cart_cart DROP CONSTRAINT IF EXISTS cart_cart_user_id_key;
ALTER TABLE IF EXISTS ONLY public.cart_cart DROP CONSTRAINT IF EXISTS cart_cart_session_key_key;
ALTER TABLE IF EXISTS ONLY public.cart_cart DROP CONSTRAINT IF EXISTS cart_cart_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
ALTER TABLE IF EXISTS ONLY public.accounts_user DROP CONSTRAINT IF EXISTS accounts_user_username_key;
ALTER TABLE IF EXISTS ONLY public.accounts_user_user_permissions DROP CONSTRAINT IF EXISTS accounts_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.accounts_user_user_permissions DROP CONSTRAINT IF EXISTS accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq;
ALTER TABLE IF EXISTS ONLY public.accounts_user DROP CONSTRAINT IF EXISTS accounts_user_pkey;
ALTER TABLE IF EXISTS ONLY public.accounts_user_groups DROP CONSTRAINT IF EXISTS accounts_user_groups_user_id_group_id_59c0b32f_uniq;
ALTER TABLE IF EXISTS ONLY public.accounts_user_groups DROP CONSTRAINT IF EXISTS accounts_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.accounts_user DROP CONSTRAINT IF EXISTS accounts_user_email_key;
ALTER TABLE IF EXISTS ONLY public.accounts_address DROP CONSTRAINT IF EXISTS accounts_address_pkey;
ALTER TABLE IF EXISTS ONLY public.account_emailconfirmation DROP CONSTRAINT IF EXISTS account_emailconfirmation_pkey;
ALTER TABLE IF EXISTS ONLY public.account_emailconfirmation DROP CONSTRAINT IF EXISTS account_emailconfirmation_key_key;
ALTER TABLE IF EXISTS ONLY public.account_emailaddress DROP CONSTRAINT IF EXISTS account_emailaddress_user_id_email_987c8728_uniq;
ALTER TABLE IF EXISTS ONLY public.account_emailaddress DROP CONSTRAINT IF EXISTS account_emailaddress_pkey;
DROP TABLE IF EXISTS public.wishlist_wishedproduct;
DROP TABLE IF EXISTS public.socialaccount_socialtoken;
DROP TABLE IF EXISTS public.socialaccount_socialapp_sites;
DROP TABLE IF EXISTS public.socialaccount_socialapp;
DROP TABLE IF EXISTS public.socialaccount_socialaccount;
DROP TABLE IF EXISTS public.repairs_repairservice;
DROP TABLE IF EXISTS public.repairs_repairbooking;
DROP TABLE IF EXISTS public.orders_orderitem;
DROP TABLE IF EXISTS public.orders_order;
DROP TABLE IF EXISTS public.django_site;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.catalog_stockmovement;
DROP TABLE IF EXISTS public.catalog_setting;
DROP TABLE IF EXISTS public.catalog_review;
DROP TABLE IF EXISTS public.catalog_qa;
DROP TABLE IF EXISTS public.catalog_productimage;
DROP TABLE IF EXISTS public.catalog_product;
DROP TABLE IF EXISTS public.catalog_homepage;
DROP TABLE IF EXISTS public.catalog_category;
DROP TABLE IF EXISTS public.catalog_brand;
DROP TABLE IF EXISTS public.catalog_adbanner;
DROP TABLE IF EXISTS public.cart_cartitem;
DROP TABLE IF EXISTS public.cart_cart;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.accounts_user_user_permissions;
DROP TABLE IF EXISTS public.accounts_user_groups;
DROP TABLE IF EXISTS public.accounts_user;
DROP TABLE IF EXISTS public.accounts_address;
DROP TABLE IF EXISTS public.account_emailconfirmation;
DROP TABLE IF EXISTS public.account_emailaddress;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account_emailaddress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_emailaddress (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    verified boolean NOT NULL,
    "primary" boolean NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.account_emailaddress OWNER TO postgres;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.account_emailaddress ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.account_emailaddress_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: account_emailconfirmation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_emailconfirmation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sent timestamp with time zone,
    key character varying(64) NOT NULL,
    email_address_id integer NOT NULL
);


ALTER TABLE public.account_emailconfirmation OWNER TO postgres;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.account_emailconfirmation ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.account_emailconfirmation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_address (
    id bigint NOT NULL,
    name character varying(120) NOT NULL,
    email character varying(254) NOT NULL,
    phone character varying(40) NOT NULL,
    address_line1 character varying(255) NOT NULL,
    address_line2 character varying(255) NOT NULL,
    city character varying(120) NOT NULL,
    postal_code character varying(20) NOT NULL,
    country character varying(80) NOT NULL,
    is_default boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.accounts_address OWNER TO postgres;

--
-- Name: accounts_address_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.accounts_address ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_address_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    referral_source character varying(64) NOT NULL,
    referral_other character varying(255) NOT NULL
);


ALTER TABLE public.accounts_user OWNER TO postgres;

--
-- Name: accounts_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.accounts_user_groups OWNER TO postgres;

--
-- Name: accounts_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.accounts_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.accounts_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.accounts_user_user_permissions OWNER TO postgres;

--
-- Name: accounts_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.accounts_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cart_cart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart_cart (
    id bigint NOT NULL,
    session_key character varying(64),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    user_id bigint,
    CONSTRAINT cart_has_owner CHECK (((user_id IS NOT NULL) OR (session_key IS NOT NULL)))
);


ALTER TABLE public.cart_cart OWNER TO postgres;

--
-- Name: cart_cart_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.cart_cart ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cart_cart_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cart_cartitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart_cartitem (
    id bigint NOT NULL,
    quantity integer NOT NULL,
    added_at timestamp with time zone NOT NULL,
    cart_id bigint NOT NULL,
    product_id bigint NOT NULL,
    CONSTRAINT cart_cartitem_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.cart_cartitem OWNER TO postgres;

--
-- Name: cart_cartitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.cart_cartitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cart_cartitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_adbanner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_adbanner (
    id bigint NOT NULL,
    title character varying(200) NOT NULL,
    "desc" character varying(300) NOT NULL,
    image character varying(200) NOT NULL,
    button character varying(80) NOT NULL,
    link character varying(300) NOT NULL,
    bg character varying(40) NOT NULL,
    "order" integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    image_file character varying(100),
    is_active boolean NOT NULL,
    button_ar character varying(80) NOT NULL,
    desc_ar character varying(300) NOT NULL,
    title_ar character varying(200) NOT NULL,
    CONSTRAINT catalog_adbanner_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.catalog_adbanner OWNER TO postgres;

--
-- Name: catalog_adbanner_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog_adbanner ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_adbanner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_brand; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_brand (
    id bigint NOT NULL,
    name character varying(120) NOT NULL,
    slug character varying(140) NOT NULL,
    logo character varying(100),
    description text NOT NULL,
    is_active boolean NOT NULL,
    "order" integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    category_id bigint,
    CONSTRAINT catalog_brand_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.catalog_brand OWNER TO postgres;

--
-- Name: catalog_brand_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog_brand ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_brand_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_category (
    id bigint NOT NULL,
    name character varying(120) NOT NULL,
    slug character varying(140) NOT NULL,
    image character varying(200) NOT NULL,
    properties jsonb NOT NULL,
    parent_id bigint,
    image_file character varying(100),
    is_active boolean NOT NULL,
    "order" integer NOT NULL,
    CONSTRAINT catalog_category_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.catalog_category OWNER TO postgres;

--
-- Name: catalog_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog_category ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_homepage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_homepage (
    id bigint NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    hero_product_id bigint
);


ALTER TABLE public.catalog_homepage OWNER TO postgres;

--
-- Name: catalog_homepage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog_homepage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_homepage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_product (
    id bigint NOT NULL,
    title character varying(200) NOT NULL,
    slug character varying(220) NOT NULL,
    description text NOT NULL,
    price numeric(10,2) NOT NULL,
    images jsonb NOT NULL,
    stock integer NOT NULL,
    color_variants jsonb NOT NULL,
    properties jsonb NOT NULL,
    brand_id bigint,
    is_featured boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    category_id bigint,
    is_active boolean NOT NULL,
    sale_price numeric(10,2),
    CONSTRAINT catalog_product_stock_check CHECK ((stock >= 0))
);


ALTER TABLE public.catalog_product OWNER TO postgres;

--
-- Name: catalog_product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog_product ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_productimage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_productimage (
    id bigint NOT NULL,
    image character varying(100) NOT NULL,
    alt character varying(200) NOT NULL,
    "order" integer NOT NULL,
    product_id bigint NOT NULL,
    CONSTRAINT catalog_productimage_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.catalog_productimage OWNER TO postgres;

--
-- Name: catalog_productimage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog_productimage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_productimage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_qa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_qa (
    id bigint NOT NULL,
    "user" character varying(120) NOT NULL,
    question text NOT NULL,
    answer text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    answered_at timestamp with time zone,
    product_id bigint NOT NULL
);


ALTER TABLE public.catalog_qa OWNER TO postgres;

--
-- Name: catalog_qa_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog_qa ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_qa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_review; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_review (
    id bigint NOT NULL,
    "user" character varying(120) NOT NULL,
    rating smallint NOT NULL,
    text text NOT NULL,
    images jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL,
    product_id bigint NOT NULL,
    CONSTRAINT catalog_review_rating_check CHECK ((rating >= 0))
);


ALTER TABLE public.catalog_review OWNER TO postgres;

--
-- Name: catalog_review_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog_review ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_setting; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_setting (
    id bigint NOT NULL,
    name character varying(120) NOT NULL,
    value jsonb NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.catalog_setting OWNER TO postgres;

--
-- Name: catalog_setting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog_setting ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_setting_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_stockmovement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalog_stockmovement (
    id bigint NOT NULL,
    delta integer NOT NULL,
    note character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    product_id bigint NOT NULL,
    user_id bigint
);


ALTER TABLE public.catalog_stockmovement OWNER TO postgres;

--
-- Name: catalog_stockmovement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.catalog_stockmovement ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_stockmovement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_site ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: orders_order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders_order (
    id bigint NOT NULL,
    reference uuid NOT NULL,
    name character varying(120) NOT NULL,
    email character varying(254) NOT NULL,
    phone character varying(40) NOT NULL,
    address_line1 character varying(255) NOT NULL,
    address_line2 character varying(255) NOT NULL,
    city character varying(120) NOT NULL,
    postal_code character varying(20) NOT NULL,
    country character varying(80) NOT NULL,
    currency character varying(8) NOT NULL,
    subtotal numeric(10,2) NOT NULL,
    total numeric(10,2) NOT NULL,
    payment_method character varying(16) NOT NULL,
    provider character varying(32) NOT NULL,
    provider_ref character varying(128) NOT NULL,
    paid boolean NOT NULL,
    status character varying(16) NOT NULL,
    referral_source character varying(64) NOT NULL,
    referral_other character varying(255) NOT NULL,
    line_items jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    user_id bigint,
    bnpl_surcharge numeric(10,2) NOT NULL,
    region character varying(3) NOT NULL,
    shipping_fee numeric(10,2) NOT NULL
);


ALTER TABLE public.orders_order OWNER TO postgres;

--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.orders_order ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.orders_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: orders_orderitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders_orderitem (
    id bigint NOT NULL,
    title character varying(200) NOT NULL,
    unit_price numeric(10,2) NOT NULL,
    quantity integer NOT NULL,
    image character varying(200) NOT NULL,
    order_id bigint NOT NULL,
    product_id bigint,
    CONSTRAINT orders_orderitem_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.orders_orderitem OWNER TO postgres;

--
-- Name: orders_orderitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.orders_orderitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.orders_orderitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: repairs_repairbooking; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.repairs_repairbooking (
    id bigint NOT NULL,
    reference uuid NOT NULL,
    name character varying(120) NOT NULL,
    email character varying(254) NOT NULL,
    phone character varying(40) NOT NULL,
    device_brand character varying(80) NOT NULL,
    device_model character varying(120) NOT NULL,
    issue text NOT NULL,
    preferred_drop_off date,
    quoted_price numeric(10,2),
    status character varying(16) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    service_id bigint
);


ALTER TABLE public.repairs_repairbooking OWNER TO postgres;

--
-- Name: repairs_repairbooking_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.repairs_repairbooking ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.repairs_repairbooking_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: repairs_repairservice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.repairs_repairservice (
    id bigint NOT NULL,
    name character varying(140) NOT NULL,
    slug character varying(160) NOT NULL,
    device character varying(12) NOT NULL,
    short_desc character varying(200) NOT NULL,
    description text NOT NULL,
    base_price numeric(10,2) NOT NULL,
    est_minutes integer NOT NULL,
    icon character varying(12) NOT NULL,
    is_featured boolean NOT NULL,
    "order" integer NOT NULL,
    CONSTRAINT repairs_repairservice_est_minutes_check CHECK ((est_minutes >= 0)),
    CONSTRAINT repairs_repairservice_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.repairs_repairservice OWNER TO postgres;

--
-- Name: repairs_repairservice_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.repairs_repairservice ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.repairs_repairservice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: socialaccount_socialaccount; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socialaccount_socialaccount (
    id integer NOT NULL,
    provider character varying(200) NOT NULL,
    uid character varying(191) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    extra_data jsonb NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.socialaccount_socialaccount OWNER TO postgres;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.socialaccount_socialaccount ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.socialaccount_socialaccount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: socialaccount_socialapp; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socialaccount_socialapp (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    name character varying(40) NOT NULL,
    client_id character varying(191) NOT NULL,
    secret character varying(191) NOT NULL,
    key character varying(191) NOT NULL,
    provider_id character varying(200) NOT NULL,
    settings jsonb NOT NULL
);


ALTER TABLE public.socialaccount_socialapp OWNER TO postgres;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.socialaccount_socialapp ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.socialaccount_socialapp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: socialaccount_socialapp_sites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socialaccount_socialapp_sites (
    id bigint NOT NULL,
    socialapp_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE public.socialaccount_socialapp_sites OWNER TO postgres;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.socialaccount_socialapp_sites ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.socialaccount_socialapp_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: socialaccount_socialtoken; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socialaccount_socialtoken (
    id integer NOT NULL,
    token text NOT NULL,
    token_secret text NOT NULL,
    expires_at timestamp with time zone,
    account_id integer NOT NULL,
    app_id integer
);


ALTER TABLE public.socialaccount_socialtoken OWNER TO postgres;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.socialaccount_socialtoken ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.socialaccount_socialtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: wishlist_wishedproduct; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wishlist_wishedproduct (
    id bigint NOT NULL,
    added_at timestamp with time zone NOT NULL,
    product_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.wishlist_wishedproduct OWNER TO postgres;

--
-- Name: wishlist_wishedproduct_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.wishlist_wishedproduct ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.wishlist_wishedproduct_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: account_emailaddress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_emailaddress (id, email, verified, "primary", user_id) FROM stdin;
\.


--
-- Data for Name: account_emailconfirmation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_emailconfirmation (id, created, sent, key, email_address_id) FROM stdin;
\.


--
-- Data for Name: accounts_address; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_address (id, name, email, phone, address_line1, address_line2, city, postal_code, country, is_default, created_at, user_id) FROM stdin;
1	Demo User		+971501234567	Sheikh Zayed Rd, Tower 1		Dubai	00000	UAE	t	2026-04-14 02:36:16.219634+04	1
2	Demo User		+971501234567	Rolla Square, Al Wahda St		Sharjah	00000	UAE	t	2026-04-14 15:55:20.611587+04	1
\.


--
-- Data for Name: accounts_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email, referral_source, referral_other) FROM stdin;
1	bcrypt_sha256$$2b$12$AlqHp/Uk0EImtzx2QVcIjeDGJaHz5VspyVuKDMMMy8yODOHW27uYi	\N	f	demo@shahzad.ae	Demo	User	f	t	2026-04-14 02:36:15.99123+04	demo@shahzad.ae		
3	bcrypt_sha256$$2b$12$VKOp970PdU9qKWacTcI9fOkZsK9HP2nAEdDOsrd3iIxhuVFBW9fJG	2026-04-29 05:57:26.77971+04	t	adibkhan			t	t	2026-04-14 10:34:30.398504+04	khanadib418@gmail.com		
2	bcrypt_sha256$$2b$12$0oOMRaYUcMpAfHhwb3lDienatoqtcmEctvJ2Vok1sBBFyB3/cGdiy	2026-05-03 22:18:31.949675+04	t	admin@shahzad.ae	Admin	User	t	t	2026-04-14 02:36:16.221913+04	admin@shahzad.ae		
4	!CvIj4YtSDXHM9xXw89j1RFgoeJUw3Wk6hu42odYz	\N	f	shahzad.qadri26@gmail.com	Shahzad	Qadri	f	t	2026-05-03 22:45:59.767252+04	shahzad.qadri26@gmail.com		
\.


--
-- Data for Name: accounts_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: accounts_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add site	6	add_site
22	Can change site	6	change_site
23	Can delete site	6	delete_site
24	Can view site	6	view_site
25	Can add email address	7	add_emailaddress
26	Can change email address	7	change_emailaddress
27	Can delete email address	7	delete_emailaddress
28	Can view email address	7	view_emailaddress
29	Can add email confirmation	8	add_emailconfirmation
30	Can change email confirmation	8	change_emailconfirmation
31	Can delete email confirmation	8	delete_emailconfirmation
32	Can view email confirmation	8	view_emailconfirmation
33	Can add social account	9	add_socialaccount
34	Can change social account	9	change_socialaccount
35	Can delete social account	9	delete_socialaccount
36	Can view social account	9	view_socialaccount
37	Can add social application	10	add_socialapp
38	Can change social application	10	change_socialapp
39	Can delete social application	10	delete_socialapp
40	Can view social application	10	view_socialapp
41	Can add social application token	11	add_socialtoken
42	Can change social application token	11	change_socialtoken
43	Can delete social application token	11	delete_socialtoken
44	Can view social application token	11	view_socialtoken
45	Can add user	12	add_user
46	Can change user	12	change_user
47	Can delete user	12	delete_user
48	Can view user	12	view_user
49	Can add address	13	add_address
50	Can change address	13	change_address
51	Can delete address	13	delete_address
52	Can view address	13	view_address
53	Can add ad banner	14	add_adbanner
54	Can change ad banner	14	change_adbanner
55	Can delete ad banner	14	delete_adbanner
56	Can view ad banner	14	view_adbanner
57	Can add setting	15	add_setting
58	Can change setting	15	change_setting
59	Can delete setting	15	delete_setting
60	Can view setting	15	view_setting
61	Can add category	16	add_category
62	Can change category	16	change_category
63	Can delete category	16	delete_category
64	Can view category	16	view_category
65	Can add product	17	add_product
66	Can change product	17	change_product
67	Can delete product	17	delete_product
68	Can view product	17	view_product
69	Can add qa	18	add_qa
70	Can change qa	18	change_qa
71	Can delete qa	18	delete_qa
72	Can view qa	18	view_qa
73	Can add review	19	add_review
74	Can change review	19	change_review
75	Can delete review	19	delete_review
76	Can view review	19	view_review
77	Can add cart	20	add_cart
78	Can change cart	20	change_cart
79	Can delete cart	20	delete_cart
80	Can view cart	20	view_cart
81	Can add cart item	21	add_cartitem
82	Can change cart item	21	change_cartitem
83	Can delete cart item	21	delete_cartitem
84	Can view cart item	21	view_cartitem
85	Can add order	22	add_order
86	Can change order	22	change_order
87	Can delete order	22	delete_order
88	Can view order	22	view_order
89	Can add order item	23	add_orderitem
90	Can change order item	23	change_orderitem
91	Can delete order item	23	delete_orderitem
92	Can view order item	23	view_orderitem
93	Can add wished product	24	add_wishedproduct
94	Can change wished product	24	change_wishedproduct
95	Can delete wished product	24	delete_wishedproduct
96	Can view wished product	24	view_wishedproduct
97	Can add repair service	25	add_repairservice
98	Can change repair service	25	change_repairservice
99	Can delete repair service	25	delete_repairservice
100	Can view repair service	25	view_repairservice
101	Can add repair booking	26	add_repairbooking
102	Can change repair booking	26	change_repairbooking
103	Can delete repair booking	26	delete_repairbooking
104	Can view repair booking	26	view_repairbooking
105	Can add product image	27	add_productimage
106	Can change product image	27	change_productimage
107	Can delete product image	27	delete_productimage
108	Can view product image	27	view_productimage
109	Can add brand	28	add_brand
110	Can change brand	28	change_brand
111	Can delete brand	28	delete_brand
112	Can view brand	28	view_brand
113	Can add Homepage	29	add_homepage
114	Can change Homepage	29	change_homepage
115	Can delete Homepage	29	delete_homepage
116	Can view Homepage	29	view_homepage
117	Can add Stock movement	30	add_stockmovement
118	Can change Stock movement	30	change_stockmovement
119	Can delete Stock movement	30	delete_stockmovement
120	Can view Stock movement	30	view_stockmovement
\.


--
-- Data for Name: cart_cart; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart_cart (id, session_key, created_at, updated_at, user_id) FROM stdin;
20	\N	2026-04-29 05:45:07.878798+04	2026-04-29 05:45:07.878798+04	3
21	\N	2026-04-29 05:55:28.999227+04	2026-04-29 05:55:28.999227+04	1
22	f0723a78-2158-45dc-9cd7-6e500182b325	2026-04-30 16:08:16.676516+04	2026-04-30 16:08:16.676516+04	\N
23	1a6dac73-2c46-47a2-84fd-ffec5e2dbe1d	2026-05-01 20:45:47.748916+04	2026-05-01 20:45:47.748916+04	\N
25	72c5d7b5-e3a6-419c-8a20-6ba6f2c30ac9	2026-05-03 22:18:21.564094+04	2026-05-03 22:18:21.564094+04	\N
27	\N	2026-05-03 22:45:59.783171+04	2026-05-03 22:45:59.783171+04	4
\.


--
-- Data for Name: cart_cartitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart_cartitem (id, quantity, added_at, cart_id, product_id) FROM stdin;
1	1	2026-05-03 22:46:15.015195+04	27	139
2	1	2026-05-03 22:51:19.481695+04	21	139
\.


--
-- Data for Name: catalog_adbanner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalog_adbanner (id, title, "desc", image, button, link, bg, "order", created_at, image_file, is_active, button_ar, desc_ar, title_ar) FROM stdin;
31	iPhone 15 Pro Max	In stock — same-day delivery across Sharjah		Shop iPhone	/products?category=smartphones	#740DC2	0	2026-04-29 05:52:49.932467+04		t			
32	Cracked screen?	Phone & laptop repairs in 30 minutes		Book a repair	/repairs	#DC2626	1	2026-04-29 05:52:49.932467+04		t			
33	MacBook bundles	Save up to AED 800 on M3 laptops		Shop laptops	/products?category=laptops	#0EA5E9	2	2026-04-29 05:52:49.932467+04		t			
34	Galaxy S24 Ultra	Free Galaxy Buds 2 Pro with every Ultra		Shop Samsung	/products?brand=samsung	#1E293B	3	2026-04-29 05:52:49.932467+04		t			
35	Pay with Tamara or Tabby	Split into 4 — interest-free		Learn how	/payment-options	#059669	4	2026-04-29 05:52:49.932467+04		t			
\.


--
-- Data for Name: catalog_brand; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalog_brand (id, name, slug, logo, description, is_active, "order", created_at, category_id) FROM stdin;
54	Apple	apple			t	0	2026-04-29 05:44:38.648135+04	22
55	Samsung	samsung			t	0	2026-04-29 05:44:38.653282+04	22
56	Google	google			t	0	2026-04-29 05:44:38.653282+04	22
57	Xiaomi	xiaomi			t	0	2026-04-29 05:44:38.658219+04	22
58	OnePlus	oneplus			t	0	2026-04-29 05:44:38.66267+04	22
59	Nothing	nothing			t	0	2026-04-29 05:44:38.66267+04	22
60	Honor	honor			t	0	2026-04-29 05:44:38.66267+04	22
61	Apple	apple-2			t	0	2026-04-29 05:44:38.673925+04	24
62	Samsung	samsung-2			t	0	2026-04-29 05:44:38.678119+04	24
63	Apple	apple-3			t	0	2026-04-29 05:44:38.678119+04	21
64	Dell	dell			t	0	2026-04-29 05:44:38.689642+04	21
65	Lenovo	lenovo			t	0	2026-04-29 05:44:38.696796+04	21
66	ASUS	asus			t	0	2026-04-29 05:44:38.700561+04	21
67	HP	hp			t	0	2026-04-29 05:44:38.700561+04	21
68	Apple	apple-4			t	0	2026-04-29 05:44:38.700561+04	18
69	Sony	sony			t	0	2026-04-29 05:44:38.714193+04	18
70	Bose	bose			t	0	2026-04-29 05:44:38.714193+04	18
71	Samsung	samsung-3			t	0	2026-04-29 05:44:38.719373+04	18
72	JBL	jbl			t	0	2026-04-29 05:44:38.719373+04	18
73	Apple	apple-5			t	0	2026-04-29 05:44:38.719373+04	25
74	Samsung	samsung-4			t	0	2026-04-29 05:44:38.72809+04	25
75	Garmin	garmin			t	0	2026-04-29 05:44:38.72809+04	25
76	Anker	anker			t	0	2026-04-29 05:44:38.72809+04	20
77	Apple	apple-6			t	0	2026-04-29 05:44:38.736063+04	20
78	Belkin	belkin			t	0	2026-04-29 05:44:38.736063+04	20
79	Apple	apple-7			t	0	2026-04-29 05:44:38.74518+04	19
80	Samsung	samsung-5			t	0	2026-04-29 05:44:38.74518+04	19
81	Spigen	spigen			t	0	2026-04-29 05:44:38.752604+04	19
82	Samsung	samsung-6			t	0	2026-04-29 05:44:38.752604+04	23
83	SanDisk	sandisk			t	0	2026-04-29 05:44:38.752604+04	23
84	WD	wd			t	0	2026-04-29 05:44:38.760795+04	23
\.


--
-- Data for Name: catalog_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalog_category (id, name, slug, image, properties, parent_id, image_file, is_active, "order") FROM stdin;
18	Audio	audio		[]	\N		t	0
19	Cases & Covers	cases-covers		[]	\N		t	0
20	Chargers & Cables	chargers-cables		[]	\N		t	0
21	Laptops	laptops		[]	\N		t	0
22	Smartphones	smartphones		[]	\N		t	0
23	Storage	storage		[]	\N		t	0
24	Tablets	tablets		[]	\N		t	0
25	Wearables	wearables		[]	\N		t	0
\.


--
-- Data for Name: catalog_homepage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalog_homepage (id, updated_at, hero_product_id) FROM stdin;
1	2026-04-29 06:00:02.440424+04	109
\.


--
-- Data for Name: catalog_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalog_product (id, title, slug, description, price, images, stock, color_variants, properties, brand_id, is_featured, created_at, updated_at, category_id, is_active, sale_price) FROM stdin;
93	iPhone 15 Pro 128GB Blue Titanium	iphone-15-pro-128gb-blue-titanium	6.1-inch Super Retina XDR OLED, A17 Pro, 48MP main camera, 3x telephoto. USB-C, Action button, titanium build. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	4099.00	["https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800"]	18	[]	{}	54	t	2026-04-29 05:44:38.760795+04	2026-04-29 05:52:49.816183+04	22	t	\N
94	iPhone 15 128GB Pink	iphone-15-128gb-pink	6.1-inch Super Retina XDR, A16 Bionic, 48MP main camera. Dynamic Island, USB-C. Includes USB-C charge cable. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	3299.00	["https://images.unsplash.com/photo-1631016800696-5ea8801b3c2a?w=800"]	25	[]	{}	54	f	2026-04-29 05:44:38.76913+04	2026-04-29 05:52:49.818041+04	22	t	3099.00
95	iPhone 14 128GB Midnight	iphone-14-128gb-midnight	6.1-inch OLED, A15 Bionic, dual 12MP camera, all-day battery. 5G, MagSafe. Excellent value flagship. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	2799.00	["https://images.unsplash.com/photo-1663499482523-1c0c1bae4ce1?w=800"]	15	[]	{}	54	f	2026-04-29 05:44:38.76913+04	2026-04-29 05:52:49.824286+04	22	t	2599.00
96	Samsung Galaxy S24 Ultra 256GB Titanium Gray	samsung-galaxy-s24-ultra-256gb-titanium-gray	6.8-inch Dynamic AMOLED 2X 120Hz, Snapdragon 8 Gen 3 for Galaxy. 200MP main + 50MP 5x periscope. Built-in S Pen, titanium frame. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	4799.00	["https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800"]	8	[]	{}	55	t	2026-04-29 05:44:38.76913+04	2026-04-29 05:52:49.824286+04	22	t	4499.00
97	Samsung Galaxy S24+ 256GB Onyx Black	samsung-galaxy-s24-256gb-onyx-black	6.7-inch Dynamic AMOLED 2X QHD+, Snapdragon 8 Gen 3, 12GB RAM. 50MP triple camera with 3x optical zoom. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	3699.00	["https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800"]	22	[]	{}	55	f	2026-04-29 05:44:38.76913+04	2026-04-29 05:52:49.824286+04	22	t	\N
98	Samsung Galaxy A55 5G 128GB Awesome Iceblue	samsung-galaxy-a55-5g-128gb-awesome-iceblue	6.6-inch Super AMOLED 120Hz, Exynos 1480, 50MP OIS main camera, 5000mAh battery. IP67 water resistance. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	1499.00	["https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800"]	50	[]	{}	55	f	2026-04-29 05:44:38.76913+04	2026-04-29 05:52:49.824286+04	22	t	1299.00
99	Google Pixel 8 Pro 128GB Bay	google-pixel-8-pro-128gb-bay	6.7-inch Super Actua LTPO 120Hz, Tensor G3 chip. Pro triple camera with 5x telephoto, Magic Eraser, Best Take. 7 years of OS updates. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	3699.00	["https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800"]	6	[]	{}	56	f	2026-04-29 05:44:38.76913+04	2026-04-29 05:52:49.839813+04	22	t	\N
100	Xiaomi 14 Ultra 512GB Black	xiaomi-14-ultra-512gb-black	Leica quad camera with 1-inch sensor, Snapdragon 8 Gen 3, 6.73-inch LTPO AMOLED. 90W wired charging. Photography flagship. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	3299.00	["https://images.unsplash.com/photo-1567581935884-3349723552ca?w=800"]	9	[]	{}	57	f	2026-04-29 05:44:38.76913+04	2026-04-29 05:52:49.839813+04	22	t	2999.00
101	OnePlus 12 256GB Silky Black	oneplus-12-256gb-silky-black	6.82-inch ProXDR LTPO 4.0, Snapdragon 8 Gen 3, 16GB RAM. Hasselblad triple camera. 100W SUPERVOOC + 50W AIRVOOC wireless. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	2899.00	["https://images.unsplash.com/photo-1546054454-aa26e2b734c7?w=800"]	14	[]	{}	58	f	2026-04-29 05:44:38.787059+04	2026-04-29 05:52:49.845997+04	22	t	\N
102	Nothing Phone (2a) 256GB Milk	nothing-phone-2a-256gb-milk	6.7-inch flexible AMOLED 120Hz, Dimensity 7200 Pro. Iconic Glyph LED interface on the back. Clean Nothing OS 2.5. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	1399.00	["https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800"]	30	[]	{}	59	t	2026-04-29 05:44:38.788013+04	2026-04-29 05:52:49.845997+04	22	t	1199.00
103	Honor Magic 6 Pro 512GB Epi Green	honor-magic-6-pro-512gb-epi-green	6.8-inch LTPO AMOLED 120Hz, Snapdragon 8 Gen 3. 180MP periscope telephoto, AI-powered Magic Capsule. 5600mAh battery. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	2999.00	["https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800"]	0	[]	{}	60	f	2026-04-29 05:44:38.788013+04	2026-04-29 05:52:49.845997+04	22	t	\N
104	iPad Pro 12.9" M2 256GB Wi-Fi Space Gray	ipad-pro-129-m2-256gb-wi-fi-space-gray	12.9-inch Liquid Retina XDR mini-LED, M2 chip, 8GB RAM. ProMotion 120Hz, Apple Pencil hover. Thunderbolt USB-C. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	4499.00	["https://images.unsplash.com/photo-1561154464-82e9adf32764?w=800"]	10	[]	{}	61	t	2026-04-29 05:44:38.788013+04	2026-04-29 05:52:49.845997+04	24	t	4199.00
105	iPad Pro 11" M4 256GB Wi-Fi Silver	ipad-pro-11-m4-256gb-wi-fi-silver	11-inch Ultra Retina XDR tandem OLED, M4 chip, 8GB RAM. Thinner design, Apple Pencil Pro support. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	3899.00	["https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=800"]	14	[]	{}	61	f	2026-04-29 05:44:38.788013+04	2026-04-29 05:52:49.856727+04	24	t	\N
106	iPad Air 11" M2 128GB Wi-Fi Blue	ipad-air-11-m2-128gb-wi-fi-blue	11-inch Liquid Retina, M2 chip, 8GB RAM. Apple Pencil Pro & USB-C Magic Keyboard support. Lighter than Pro. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	2499.00	["https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=800"]	20	[]	{}	61	f	2026-04-29 05:44:38.788013+04	2026-04-29 05:52:49.85928+04	24	t	2299.00
107	iPad 10th Gen 64GB Wi-Fi Silver	ipad-10th-gen-64gb-wi-fi-silver	10.9-inch Liquid Retina, A14 Bionic, USB-C, landscape FaceTime camera. Best-value iPad for everyday use. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	1499.00	["https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800"]	35	[]	{}	61	f	2026-04-29 05:44:38.800641+04	2026-04-29 05:52:49.862347+04	24	t	\N
108	Samsung Galaxy Tab S9 Ultra 256GB Wi-Fi Graphite	samsung-galaxy-tab-s9-ultra-256gb-wi-fi-graphite	14.6-inch Dynamic AMOLED 2X 120Hz, Snapdragon 8 Gen 2 for Galaxy. Includes S Pen. IP68 water resistance. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	3999.00	["https://images.unsplash.com/photo-1542751110-97427bbecf20?w=800"]	7	[]	{}	62	f	2026-04-29 05:44:38.802025+04	2026-04-29 05:52:49.862347+04	24	t	\N
110	MacBook Air 13" M3 16GB / 256GB Midnight	macbook-air-13-m3-16gb-256gb-midnight	13.6-inch Liquid Retina, M3 chip 8-core CPU, 10-core GPU. Up to 18 hours battery. Fanless silent design. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	4999.00	["https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800"]	12	[]	{}	63	f	2026-04-29 05:44:38.802025+04	2026-04-29 05:52:49.862347+04	21	t	\N
111	MacBook Air 15" M2 8GB / 256GB Starlight	macbook-air-15-m2-8gb-256gb-starlight	15.3-inch Liquid Retina, M2 chip. Six-speaker sound system, MagSafe charging. Largest-screen Air. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	4699.00	["https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800"]	8	[]	{}	63	f	2026-04-29 05:44:38.802025+04	2026-04-29 05:52:49.870396+04	21	t	4399.00
112	Dell XPS 15 OLED Core i7 / 32GB / 1TB	dell-xps-15-oled-core-i7-32gb-1tb	15.6-inch 3.5K OLED InfinityEdge touchscreen. Intel Core i7-13700H, RTX 4060, 32GB DDR5, 1TB NVMe. CNC machined aluminum. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	7299.00	["https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=800"]	4	[]	{}	64	f	2026-04-29 05:44:38.802025+04	2026-04-29 05:52:49.87193+04	21	t	\N
113	Lenovo ThinkPad X1 Carbon Gen 12 Core i7 / 16GB / 1TB	lenovo-thinkpad-x1-carbon-gen-12-core-i7-16gb-1tb	14-inch 2.8K OLED, Intel Core Ultra 7. 16GB LPDDR5X, 1TB SSD. MIL-SPEC durability, ThinkShutter privacy. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	6499.00	["https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800"]	6	[]	{}	65	f	2026-04-29 05:44:38.802025+04	2026-04-29 05:52:49.87193+04	21	t	5999.00
114	ASUS ROG Zephyrus G14 Ryzen 9 / RTX 4060 / 1TB	asus-rog-zephyrus-g14-ryzen-9-rtx-4060-1tb	14-inch QHD+ OLED 120Hz Nebula display. Ryzen 9 8945HS, RTX 4060, 16GB DDR5, 1TB NVMe. AniMe Matrix LED lid. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	5999.00	["https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800"]	3	[]	{}	66	f	2026-04-29 05:44:38.802025+04	2026-04-29 05:52:49.87193+04	21	t	\N
115	HP Spectre x360 14 Core Ultra 7 / 16GB / 1TB	hp-spectre-x360-14-core-ultra-7-16gb-1tb	14-inch 2.8K OLED touch convertible. Core Ultra 7 155H, 16GB LPDDR5x, 1TB. Includes HP MPP2.0 tilt pen. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	5499.00	["https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800"]	5	[]	{}	67	f	2026-04-29 05:44:38.817359+04	2026-04-29 05:52:49.878532+04	21	t	\N
116	AirPods Pro 2 (USB-C)	airpods-pro-2-usb-c	Adaptive Audio, Active Noise Cancellation, Conversation Awareness. Up to 30 hours with charging case. USB-C MagSafe case. Sealed retail box, 1-year manufacturer warranty. Free delivery across the UAE.	899.00	["https://images.unsplash.com/photo-1606220838315-056192d5e927?w=800"]	40	[]	{}	68	t	2026-04-29 05:44:38.817359+04	2026-04-29 05:52:49.878532+04	18	t	799.00
117	AirPods Max Space Gray	airpods-max-space-gray	Over-ear, computational audio, Spatial Audio with dynamic head tracking. 20-hour battery. Premium aluminum + memory foam. Sealed retail box, 1-year manufacturer warranty. Free delivery across the UAE.	2299.00	["https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=800"]	8	[]	{}	68	f	2026-04-29 05:44:38.817359+04	2026-04-29 05:52:49.878532+04	18	t	\N
118	AirPods 4 with Active Noise Cancellation	airpods-4-with-active-noise-cancellation	Open-ear design with H2 chip ANC. Personalized Spatial Audio, Voice Isolation. Wireless charging case. Sealed retail box, 1-year manufacturer warranty. Free delivery across the UAE.	799.00	["https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=800"]	25	[]	{}	68	f	2026-04-29 05:44:38.817359+04	2026-04-29 05:52:49.878532+04	18	t	\N
119	Sony WH-1000XM5 Black	sony-wh-1000xm5-black	Industry-leading noise cancellation, 8 microphones. 30-hour battery, LDAC + DSEE Extreme. Multipoint Bluetooth. Sealed retail box, 1-year manufacturer warranty. Free delivery across the UAE.	1399.00	["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"]	12	[]	{}	69	f	2026-04-29 05:44:38.817359+04	2026-04-29 05:52:49.878532+04	18	t	1199.00
120	Sony WF-1000XM5	sony-wf-1000xm5	Smallest, lightest XM-series in-ears. Integrated processor V2 + V1. 8-hour battery (24 with case). Crystal-clear calls. Sealed retail box, 1-year manufacturer warranty. Free delivery across the UAE.	1199.00	["https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800"]	18	[]	{}	69	f	2026-04-29 05:44:38.817359+04	2026-04-29 05:52:49.878532+04	18	t	\N
121	Bose QuietComfort Ultra Headphones	bose-quietcomfort-ultra-headphones	Immersive Audio with Spatial-aware playback. World-class noise cancellation. 24-hour battery, plush memory foam earcups. Sealed retail box, 1-year manufacturer warranty. Free delivery across the UAE.	1599.00	["https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800"]	6	[]	{}	70	f	2026-04-29 05:44:38.817359+04	2026-04-29 05:52:49.878532+04	18	t	\N
122	Samsung Galaxy Buds 2 Pro	samsung-galaxy-buds-2-pro	Hi-Fi 24-bit audio, intelligent ANC, 360 Audio. IPX7 water resistance. Seamless switching across Galaxy devices. Sealed retail box, 1-year manufacturer warranty. Free delivery across the UAE.	799.00	["https://images.unsplash.com/photo-1606220838315-056192d5e927?w=800"]	22	[]	{}	71	f	2026-04-29 05:44:38.832209+04	2026-04-29 05:52:49.896158+04	18	t	649.00
123	JBL Charge 5 Bluetooth Speaker Black	jbl-charge-5-bluetooth-speaker-black	20-hour playtime, IP67 dust/water proof. Built-in powerbank to charge your phone. PartyBoost to pair multiple JBLs. Sealed retail box, 1-year manufacturer warranty. Free delivery across the UAE.	599.00	["https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800"]	30	[]	{}	72	f	2026-04-29 05:44:38.832209+04	2026-04-29 05:52:49.90128+04	18	t	499.00
124	Apple Watch Ultra 2 49mm Titanium Trail Loop	apple-watch-ultra-2-49mm-titanium-trail-loop	Brightest-ever Apple Watch display, S9 chip. Action button, Dive computer, GPS precision dual-frequency. Up to 36-hour battery. Sealed retail box, 1-year manufacturer warranty. Free delivery and band-fit help in store.	3299.00	["https://images.unsplash.com/photo-1551816230-ef5deaed4a26?w=800"]	6	[]	{}	73	t	2026-04-29 05:44:38.832209+04	2026-04-29 05:52:49.90128+04	25	t	\N
125	Apple Watch Series 9 GPS 41mm Midnight	apple-watch-series-9-gps-41mm-midnight	S9 chip, Double Tap gesture, brighter display. ECG, Blood Oxygen, temperature sensing. Sealed retail box, 1-year manufacturer warranty. Free delivery and band-fit help in store.	1499.00	["https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800"]	18	[]	{}	73	f	2026-04-29 05:44:38.832209+04	2026-04-29 05:52:49.90128+04	25	t	1299.00
92	iPhone 15 Pro Max 256GB Natural Titanium	iphone-15-pro-max-256gb-natural-titanium	6.7-inch Super Retina XDR OLED with ProMotion. A17 Pro chip, 48MP main + 5x telephoto. Titanium frame, USB-C, Action button. Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide.	4699.00	["https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800"]	12	[]	{}	54	t	2026-04-29 05:44:38.760795+04	2026-04-29 05:52:49.808736+04	22	t	\N
109	MacBook Pro 14" M3 Pro 18GB / 512GB Space Black	macbook-pro-14-m3-pro-18gb-512gb-space-black	14-inch Liquid Retina XDR mini-LED 120Hz. M3 Pro: 11-core CPU, 14-core GPU. Up to 18 hours battery. Includes 70W USB-C adapter. Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request.	8999.00	["https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800"]	5	[]	{}	63	t	2026-04-29 05:44:38.802025+04	2026-04-29 05:52:49.862347+04	21	t	8499.00
126	Apple Watch SE 2nd Gen 40mm Starlight	apple-watch-se-2nd-gen-40mm-starlight	S8 chip, all the essentials at a friendlier price. Crash and Fall detection, fitness tracking, family setup. Sealed retail box, 1-year manufacturer warranty. Free delivery and band-fit help in store.	999.00	["https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800"]	30	[]	{}	73	f	2026-04-29 05:44:38.832209+04	2026-04-29 05:52:49.907854+04	25	t	\N
127	Samsung Galaxy Watch 6 Classic 47mm	samsung-galaxy-watch-6-classic-47mm	Rotating bezel returns. Sleep Insights, advanced workout tracking, body composition analysis. Wear OS 4. Sealed retail box, 1-year manufacturer warranty. Free delivery and band-fit help in store.	1399.00	["https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800"]	10	[]	{}	74	f	2026-04-29 05:44:38.832209+04	2026-04-29 05:52:49.907854+04	25	t	\N
128	Garmin Fenix 7 Sapphire Solar Titanium	garmin-fenix-7-sapphire-solar-titanium	Solar-charging multisport GPS. Built for the toughest adventures. Up to 22 days battery, multi-band GNSS. Sealed retail box, 1-year manufacturer warranty. Free delivery and band-fit help in store.	3899.00	["https://images.unsplash.com/photo-1617043786394-f977fa12eddf?w=800"]	4	[]	{}	75	f	2026-04-29 05:44:38.832209+04	2026-04-29 05:52:49.907854+04	25	t	\N
129	Anker 65W GaN II 3-Port Charger	anker-65w-gan-ii-3-port-charger	65W total across two USB-C and one USB-A. Fast-charge MacBook Air, iPad Pro, iPhone simultaneously. Foldable plug. 1-year warranty. Free delivery on orders over AED 100.	189.00	["https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800"]	60	[]	{}	76	f	2026-04-29 05:44:38.852333+04	2026-04-29 05:52:49.907854+04	20	t	159.00
130	Apple 20W USB-C Power Adapter	apple-20w-usb-c-power-adapter	Fast-charges iPhone 8 and later up to 50% in 30 minutes. Compact, single USB-C port. Cable sold separately. 1-year warranty. Free delivery on orders over AED 100.	89.00	["https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=800"]	100	[]	{}	77	f	2026-04-29 05:44:38.855555+04	2026-04-29 05:52:49.91599+04	20	t	\N
131	Apple MagSafe Charger 1m	apple-magsafe-charger-1m	Up to 15W wireless charging for iPhone 12 and later. Magnetic alignment, USB-C connector. Power adapter not included. 1-year warranty. Free delivery on orders over AED 100.	159.00	["https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=800"]	45	[]	{}	77	f	2026-04-29 05:44:38.855555+04	2026-04-29 05:52:49.91599+04	20	t	\N
132	Belkin BoostCharge Pro 3-in-1 MagSafe Wireless Stand	belkin-boostcharge-pro-3-in-1-magsafe-wireless-stand	Charges iPhone 15W MagSafe, Apple Watch fast-charge, AirPods at the same time. Premium aluminum stand. 1-year warranty. Free delivery on orders over AED 100.	599.00	["https://images.unsplash.com/photo-1593642533144-3d62aa4783ec?w=800"]	12	[]	{}	78	f	2026-04-29 05:44:38.855555+04	2026-04-29 05:52:49.91599+04	20	t	\N
133	iPhone 15 Pro Silicone Case with MagSafe — Cypress	iphone-15-pro-silicone-case-with-magsafe-cypress	Apple silicone with soft microfibre lining. Built-in magnets align with MagSafe accessories. Slim, grippy. 1-year warranty. Free delivery on orders over AED 100.	189.00	["https://images.unsplash.com/photo-1601972602288-3be527b4f18a?w=800"]	35	[]	{}	79	f	2026-04-29 05:44:38.864079+04	2026-04-29 05:52:49.91599+04	19	t	\N
134	Samsung Galaxy S24 Ultra Smart View Wallet Case	samsung-galaxy-s24-ultra-smart-view-wallet-case	View notifications and answer calls without opening. Card slot, kickstand. Genuine Samsung accessory. 1-year warranty. Free delivery on orders over AED 100.	179.00	["https://images.unsplash.com/photo-1601972602288-3be527b4f18a?w=800"]	25	[]	{}	80	f	2026-04-29 05:44:38.864079+04	2026-04-29 05:52:49.91599+04	19	t	\N
135	Spigen Tough Armor MacBook Pro 14" Sleeve	spigen-tough-armor-macbook-pro-14-sleeve	Microfibre interior, water-resistant exterior, magnetic flap closure. Front pocket for charger and dongles. 1-year warranty. Free delivery on orders over AED 100.	159.00	["https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800"]	20	[]	{}	81	f	2026-04-29 05:44:38.864079+04	2026-04-29 05:52:49.924575+04	19	t	129.00
136	Samsung T7 Shield 1TB Portable SSD Black	samsung-t7-shield-1tb-portable-ssd-black	Up to 1,050 MB/s read, 1,000 MB/s write. IP65 dust/water resistant, drop-tested to 3m. USB 3.2 Gen 2 USB-C. 1-year warranty. Free delivery on orders over AED 100.	449.00	["https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800"]	28	[]	{}	82	f	2026-04-29 05:44:38.864079+04	2026-04-29 05:52:49.924575+04	23	t	399.00
137	SanDisk Extreme microSDXC 256GB	sandisk-extreme-microsdxc-256gb	Up to 190MB/s read, 130MB/s write. A2, V30, U3 — perfect for 4K UHD video and Nintendo Switch. Includes SD adapter. 1-year warranty. Free delivery on orders over AED 100.	159.00	["https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800"]	80	[]	{}	83	f	2026-04-29 05:44:38.864079+04	2026-04-29 05:52:49.924575+04	23	t	\N
138	WD My Passport 4TB External Hard Drive	wd-my-passport-4tb-external-hard-drive	USB 3.2 Gen 1, 256-bit AES hardware encryption. Auto backup with WD Backup software. Plug-and-play on Windows; reformat for macOS. 1-year warranty. Free delivery on orders over AED 100.	399.00	["https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800"]	18	[]	{}	84	f	2026-04-29 05:44:38.864079+04	2026-04-29 05:52:49.924575+04	23	t	\N
139	test product	test-product	test-product for 1 dirham	999.00	[]	9	[]	{}	54	f	2026-05-03 22:41:57.358315+04	2026-05-03 22:41:57.358315+04	22	t	1.00
\.


--
-- Data for Name: catalog_productimage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalog_productimage (id, image, alt, "order", product_id) FROM stdin;
\.


--
-- Data for Name: catalog_qa; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalog_qa (id, "user", question, answer, created_at, answered_at, product_id) FROM stdin;
\.


--
-- Data for Name: catalog_review; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalog_review (id, "user", rating, text, images, created_at, product_id) FROM stdin;
372	Ahmed K.	5	Exactly as described — arrived next day. Would buy again.	[]	2026-04-29 05:44:38.963612+04	133
373	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:38.967633+04	133
374	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:38.969644+04	138
375	Omar R.	5	Honest shop, good warranty, trustworthy.	[]	2026-04-29 05:44:38.971656+04	138
376	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:38.971656+04	138
377	Reem H.	5	Trade-in value was fair. Smooth process.	[]	2026-04-29 05:44:38.975628+04	137
378	Fatima S.	5	Great service and fast delivery to Sharjah. Packaged well.	[]	2026-04-29 05:44:38.977785+04	137
379	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:38.977785+04	136
380	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:38.977785+04	136
381	Ahmed K.	5	Exactly as described — arrived next day. Would buy again.	[]	2026-04-29 05:44:38.977785+04	135
382	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:38.985416+04	135
383	Reem H.	5	Trade-in value was fair. Smooth process.	[]	2026-04-29 05:44:38.985416+04	135
384	Tariq F.	4	Good experience overall. Slight delay but worth it.	[]	2026-04-29 05:44:38.987478+04	134
385	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:38.990324+04	134
386	Ahmed K.	5	Exactly as described — arrived next day. Would buy again.	[]	2026-04-29 05:44:38.990324+04	134
387	Reem H.	5	Trade-in value was fair. Smooth process.	[]	2026-04-29 05:44:38.994386+04	130
388	Yousef A.	5	Best price I found in Sharjah. Will come again.	[]	2026-04-29 05:44:38.995319+04	130
389	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:38.995903+04	130
390	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:38.995903+04	132
391	Yousef A.	5	Best price I found in Sharjah. Will come again.	[]	2026-04-29 05:44:38.995903+04	132
392	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:38.995903+04	132
393	Saleh M.	5	Quality product, exactly as advertised. 5 stars.	[]	2026-04-29 05:44:38.995903+04	131
394	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:38.995903+04	131
395	Mariam K.	4	Very happy with the purchase. Delivery was same day.	[]	2026-04-29 05:44:38.995903+04	129
396	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:38.995903+04	129
397	Fatima S.	5	Great service and fast delivery to Sharjah. Packaged well.	[]	2026-04-29 05:44:38.995903+04	129
398	Tariq F.	4	Good experience overall. Slight delay but worth it.	[]	2026-04-29 05:44:38.995903+04	129
399	Saleh M.	5	Quality product, exactly as advertised. 5 stars.	[]	2026-04-29 05:44:38.995903+04	123
400	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:38.995903+04	123
401	Mariam K.	4	Very happy with the purchase. Delivery was same day.	[]	2026-04-29 05:44:38.995903+04	128
402	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:38.995903+04	128
403	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:38.995903+04	128
404	Fatima S.	5	Great service and fast delivery to Sharjah. Packaged well.	[]	2026-04-29 05:44:38.995903+04	128
405	Noura Z.	5	Genuine product, came sealed. Customer service was excellent.	[]	2026-04-29 05:44:38.995903+04	127
406	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:38.995903+04	127
407	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:38.995903+04	127
408	Saleh M.	5	Quality product, exactly as advertised. 5 stars.	[]	2026-04-29 05:44:39.010172+04	126
409	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:39.01115+04	126
410	Mariam K.	4	Very happy with the purchase. Delivery was same day.	[]	2026-04-29 05:44:39.01115+04	125
411	Zara M.	4	Exactly what I expected. Price is fair.	[]	2026-04-29 05:44:39.01115+04	125
412	Mariam K.	4	Very happy with the purchase. Delivery was same day.	[]	2026-04-29 05:44:39.01115+04	125
413	Mariam K.	4	Very happy with the purchase. Delivery was same day.	[]	2026-04-29 05:44:39.01115+04	125
414	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:39.01115+04	125
415	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.01115+04	124
416	Zara M.	4	Exactly what I expected. Price is fair.	[]	2026-04-29 05:44:39.01115+04	124
417	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:39.01115+04	124
418	Zara M.	4	Exactly what I expected. Price is fair.	[]	2026-04-29 05:44:39.01115+04	124
419	Saleh M.	5	Quality product, exactly as advertised. 5 stars.	[]	2026-04-29 05:44:39.018517+04	122
420	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:39.018517+04	122
421	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:39.018517+04	122
422	Yousef A.	5	Best price I found in Sharjah. Will come again.	[]	2026-04-29 05:44:39.018517+04	122
423	Fatima S.	5	Great service and fast delivery to Sharjah. Packaged well.	[]	2026-04-29 05:44:39.018517+04	122
424	Fatima S.	5	Great service and fast delivery to Sharjah. Packaged well.	[]	2026-04-29 05:44:39.018517+04	120
425	Yousef A.	5	Best price I found in Sharjah. Will come again.	[]	2026-04-29 05:44:39.018517+04	120
426	Saleh M.	5	Quality product, exactly as advertised. 5 stars.	[]	2026-04-29 05:44:39.018517+04	120
427	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.018517+04	115
428	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:39.018517+04	115
429	Yousef A.	5	Best price I found in Sharjah. Will come again.	[]	2026-04-29 05:44:39.018517+04	115
430	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:39.018517+04	115
431	Saleh M.	5	Quality product, exactly as advertised. 5 stars.	[]	2026-04-29 05:44:39.026816+04	116
432	Tariq F.	4	Good experience overall. Slight delay but worth it.	[]	2026-04-29 05:44:39.026816+04	116
433	Omar R.	5	Honest shop, good warranty, trustworthy.	[]	2026-04-29 05:44:39.027913+04	116
434	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:39.027913+04	116
435	Omar R.	5	Honest shop, good warranty, trustworthy.	[]	2026-04-29 05:44:39.027913+04	116
436	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:39.027913+04	117
437	Reem H.	5	Trade-in value was fair. Smooth process.	[]	2026-04-29 05:44:39.027913+04	117
438	Saleh M.	5	Quality product, exactly as advertised. 5 stars.	[]	2026-04-29 05:44:39.027913+04	117
439	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:39.027913+04	118
440	Omar R.	5	Honest shop, good warranty, trustworthy.	[]	2026-04-29 05:44:39.027913+04	118
441	Hessa A.	5	Highly recommend — they explain everything clearly.	[]	2026-04-29 05:44:39.027913+04	118
442	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.027913+04	118
443	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.035274+04	119
444	Omar R.	5	Honest shop, good warranty, trustworthy.	[]	2026-04-29 05:44:39.035274+04	119
445	Reem H.	5	Trade-in value was fair. Smooth process.	[]	2026-04-29 05:44:39.035274+04	121
446	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.035274+04	121
447	Saleh M.	5	Quality product, exactly as advertised. 5 stars.	[]	2026-04-29 05:44:39.035274+04	121
448	Tariq F.	4	Good experience overall. Slight delay but worth it.	[]	2026-04-29 05:44:39.035274+04	108
449	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:39.035274+04	108
450	Ahmed K.	5	Exactly as described — arrived next day. Would buy again.	[]	2026-04-29 05:44:39.035274+04	108
451	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.035274+04	108
452	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:39.035274+04	108
453	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.035274+04	114
454	Noura Z.	5	Genuine product, came sealed. Customer service was excellent.	[]	2026-04-29 05:44:39.035274+04	114
455	Reem H.	5	Trade-in value was fair. Smooth process.	[]	2026-04-29 05:44:39.035274+04	114
456	Zara M.	4	Exactly what I expected. Price is fair.	[]	2026-04-29 05:44:39.043649+04	114
457	Ahmed K.	5	Exactly as described — arrived next day. Would buy again.	[]	2026-04-29 05:44:39.043649+04	113
458	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:39.043649+04	113
459	Zara M.	4	Exactly what I expected. Price is fair.	[]	2026-04-29 05:44:39.043649+04	113
460	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.043649+04	113
461	Noura Z.	5	Genuine product, came sealed. Customer service was excellent.	[]	2026-04-29 05:44:39.043649+04	113
462	Omar R.	5	Honest shop, good warranty, trustworthy.	[]	2026-04-29 05:44:39.043649+04	110
463	Mariam K.	4	Very happy with the purchase. Delivery was same day.	[]	2026-04-29 05:44:39.043649+04	110
464	Zara M.	4	Exactly what I expected. Price is fair.	[]	2026-04-29 05:44:39.043649+04	110
465	Yousef A.	5	Best price I found in Sharjah. Will come again.	[]	2026-04-29 05:44:39.043649+04	111
466	Hessa A.	5	Highly recommend — they explain everything clearly.	[]	2026-04-29 05:44:39.043649+04	111
467	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.052021+04	112
468	Mariam K.	4	Very happy with the purchase. Delivery was same day.	[]	2026-04-29 05:44:39.052021+04	112
469	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:39.052021+04	109
470	Fatima S.	5	Great service and fast delivery to Sharjah. Packaged well.	[]	2026-04-29 05:44:39.052021+04	109
471	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:39.052021+04	109
472	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.052021+04	109
473	Hessa A.	5	Highly recommend — they explain everything clearly.	[]	2026-04-29 05:44:39.052021+04	107
474	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.052021+04	107
475	Omar R.	5	Honest shop, good warranty, trustworthy.	[]	2026-04-29 05:44:39.052021+04	102
476	Hessa A.	5	Highly recommend — they explain everything clearly.	[]	2026-04-29 05:44:39.052021+04	102
477	Zara M.	4	Exactly what I expected. Price is fair.	[]	2026-04-29 05:44:39.052021+04	102
478	Reem H.	5	Trade-in value was fair. Smooth process.	[]	2026-04-29 05:44:39.052021+04	106
479	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:39.052021+04	106
480	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:39.052021+04	106
481	Noura Z.	5	Genuine product, came sealed. Customer service was excellent.	[]	2026-04-29 05:44:39.052021+04	106
482	Mariam K.	4	Very happy with the purchase. Delivery was same day.	[]	2026-04-29 05:44:39.052021+04	105
483	Tariq F.	4	Good experience overall. Slight delay but worth it.	[]	2026-04-29 05:44:39.052021+04	105
484	Tariq F.	4	Good experience overall. Slight delay but worth it.	[]	2026-04-29 05:44:39.052021+04	105
485	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.052021+04	105
486	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:39.052021+04	105
487	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.068151+04	104
488	Yousef A.	5	Best price I found in Sharjah. Will come again.	[]	2026-04-29 05:44:39.069298+04	104
489	Ahmed K.	5	Exactly as described — arrived next day. Would buy again.	[]	2026-04-29 05:44:39.070065+04	104
490	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:39.070065+04	103
491	Ahmed K.	5	Exactly as described — arrived next day. Would buy again.	[]	2026-04-29 05:44:39.070065+04	103
492	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.070065+04	103
493	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:39.070065+04	101
494	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.070065+04	101
495	Yousef A.	5	Best price I found in Sharjah. Will come again.	[]	2026-04-29 05:44:39.070065+04	98
496	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.070065+04	98
497	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:39.070065+04	96
498	Hessa A.	5	Highly recommend — they explain everything clearly.	[]	2026-04-29 05:44:39.070065+04	96
499	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:39.070065+04	96
500	Hessa A.	5	Highly recommend — they explain everything clearly.	[]	2026-04-29 05:44:39.070065+04	95
501	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:39.070065+04	95
502	Hessa A.	5	Highly recommend — they explain everything clearly.	[]	2026-04-29 05:44:39.070065+04	95
503	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:39.070065+04	94
504	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.070065+04	94
505	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.070065+04	94
506	Reem H.	5	Trade-in value was fair. Smooth process.	[]	2026-04-29 05:44:39.070065+04	94
507	Mariam K.	4	Very happy with the purchase. Delivery was same day.	[]	2026-04-29 05:44:39.070065+04	94
508	Reem H.	5	Trade-in value was fair. Smooth process.	[]	2026-04-29 05:44:39.085241+04	100
509	Tariq F.	4	Good experience overall. Slight delay but worth it.	[]	2026-04-29 05:44:39.085241+04	100
510	Fatima S.	5	Great service and fast delivery to Sharjah. Packaged well.	[]	2026-04-29 05:44:39.085241+04	100
511	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.087456+04	100
512	Fatima S.	5	Great service and fast delivery to Sharjah. Packaged well.	[]	2026-04-29 05:44:39.088006+04	100
513	Yousef A.	5	Best price I found in Sharjah. Will come again.	[]	2026-04-29 05:44:39.090185+04	99
514	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.090185+04	99
515	Aisha N.	5	Called for repair quote — they picked up within seconds.	[]	2026-04-29 05:44:39.090185+04	99
516	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:39.0943+04	99
517	Hassan T.	5	Tried Tamara, approval was instant. Very smooth checkout.	[]	2026-04-29 05:44:39.09523+04	99
518	Omar R.	5	Honest shop, good warranty, trustworthy.	[]	2026-04-29 05:44:39.09523+04	97
519	Reem H.	5	Trade-in value was fair. Smooth process.	[]	2026-04-29 05:44:39.09523+04	97
520	Zara M.	4	Exactly what I expected. Price is fair.	[]	2026-04-29 05:44:39.09523+04	97
521	Khalid B.	4	Solid product. Came with all accessories. Recommended.	[]	2026-04-29 05:44:39.09523+04	97
522	Tariq F.	4	Good experience overall. Slight delay but worth it.	[]	2026-04-29 05:44:39.09523+04	97
523	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.09523+04	92
524	Tariq F.	4	Good experience overall. Slight delay but worth it.	[]	2026-04-29 05:44:39.09523+04	92
525	Layla H.	5	Perfect condition, sealed box, best price in UAE.	[]	2026-04-29 05:44:39.09523+04	92
526	Ahmed K.	5	Exactly as described — arrived next day. Would buy again.	[]	2026-04-29 05:44:39.102427+04	93
527	Mohammed A.	4	Good product but came a day late. Still recommend.	[]	2026-04-29 05:44:39.102427+04	93
\.


--
-- Data for Name: catalog_setting; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalog_setting (id, name, value, updated_at) FROM stdin;
\.


--
-- Data for Name: catalog_stockmovement; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalog_stockmovement (id, delta, note, created_at, product_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2026-04-14 13:35:36.119447+04	6	Cart object (6)	3		20	2
2	2026-04-14 13:35:36.119447+04	5	Cart object (5)	3		20	2
3	2026-04-14 13:35:36.119447+04	4	Cart object (4)	3		20	2
4	2026-04-14 13:35:36.119447+04	2	Cart object (2)	3		20	2
5	2026-04-14 13:35:36.119447+04	1	Cart object (1)	3		20	2
6	2026-04-14 13:35:46.833485+04	3	Order 1e8dbe93	3		22	2
7	2026-04-14 13:35:46.833485+04	2	Order 089cd8dc	3		22	2
8	2026-04-14 13:35:46.833485+04	1	Order 581d71dc	3		22	2
9	2026-04-14 14:22:02.378283+04	7	Cart object (7)	3		20	2
10	2026-04-19 01:15:58.267282+04	24	Samsung Galaxy S24 Ultra	2	[{"changed": {"fields": ["Is featured"]}}]	17	2
11	2026-04-19 01:34:42.681044+04	1	Homepage	2	[{"changed": {"fields": ["Hero product"]}}]	29	2
12	2026-04-19 01:35:03.552437+04	1	Homepage	2	[{"changed": {"fields": ["Hero product"]}}]	29	2
13	2026-04-19 01:35:24.242436+04	1	Homepage	2	[{"changed": {"fields": ["Hero product"]}}]	29	2
14	2026-04-19 01:39:47.729329+04	1	Homepage	2	[{"changed": {"fields": ["Hero product"]}}]	29	2
15	2026-04-19 23:48:40.598081+04	10	New iPhone 15 Pro	2	[{"changed": {"fields": ["Title ar", "Desc ar", "Button ar"]}}]	14	2
16	2026-04-29 05:58:57.599553+04	1	Homepage	2	[{"changed": {"fields": ["Hero product"]}}]	29	3
17	2026-04-29 05:59:23.448884+04	1	Homepage	2	[{"changed": {"fields": ["Hero product"]}}]	29	3
18	2026-04-29 06:00:02.445227+04	1	Homepage	2	[{"changed": {"fields": ["Hero product"]}}]	29	3
19	2026-05-03 22:41:57.395406+04	139	test product	1	[{"added": {}}]	17	2
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	sites	site
7	account	emailaddress
8	account	emailconfirmation
9	socialaccount	socialaccount
10	socialaccount	socialapp
11	socialaccount	socialtoken
12	accounts	user
13	accounts	address
14	catalog	adbanner
15	catalog	setting
16	catalog	category
17	catalog	product
18	catalog	qa
19	catalog	review
20	cart	cart
21	cart	cartitem
22	orders	order
23	orders	orderitem
24	wishlist	wishedproduct
25	repairs	repairservice
26	repairs	repairbooking
27	catalog	productimage
28	catalog	brand
29	catalog	homepage
30	catalog	stockmovement
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-04-14 01:37:46.864172+04
2	contenttypes	0002_remove_content_type_name	2026-04-14 01:37:46.871258+04
3	auth	0001_initial	2026-04-14 01:37:46.920991+04
4	auth	0002_alter_permission_name_max_length	2026-04-14 01:37:46.928559+04
5	auth	0003_alter_user_email_max_length	2026-04-14 01:37:46.934014+04
6	auth	0004_alter_user_username_opts	2026-04-14 01:37:46.937038+04
7	auth	0005_alter_user_last_login_null	2026-04-14 01:37:46.943212+04
8	auth	0006_require_contenttypes_0002	2026-04-14 01:37:46.945202+04
9	auth	0007_alter_validators_add_error_messages	2026-04-14 01:37:46.950615+04
10	auth	0008_alter_user_username_max_length	2026-04-14 01:37:46.955854+04
11	auth	0009_alter_user_last_name_max_length	2026-04-14 01:37:46.960991+04
12	auth	0010_alter_group_name_max_length	2026-04-14 01:37:46.969585+04
13	auth	0011_update_proxy_permissions	2026-04-14 01:37:46.973049+04
14	auth	0012_alter_user_first_name_max_length	2026-04-14 01:37:46.973049+04
15	accounts	0001_initial	2026-04-14 01:37:47.021454+04
16	account	0001_initial	2026-04-14 01:37:47.051399+04
17	account	0002_email_max_length	2026-04-14 01:37:47.064073+04
18	account	0003_alter_emailaddress_create_unique_verified_email	2026-04-14 01:37:47.082151+04
19	account	0004_alter_emailaddress_drop_unique_email	2026-04-14 01:37:47.090972+04
20	account	0005_emailaddress_idx_upper_email	2026-04-14 01:37:47.104897+04
21	account	0006_emailaddress_lower	2026-04-14 01:37:47.121393+04
22	account	0007_emailaddress_idx_email	2026-04-14 01:37:47.141176+04
23	account	0008_emailaddress_unique_primary_email_fixup	2026-04-14 01:37:47.180952+04
24	account	0009_emailaddress_unique_primary_email	2026-04-14 01:37:47.191054+04
25	accounts	0002_address	2026-04-14 01:37:47.202169+04
26	admin	0001_initial	2026-04-14 01:37:47.22107+04
27	admin	0002_logentry_remove_auto_add	2026-04-14 01:37:47.233078+04
28	admin	0003_logentry_add_action_flag_choices	2026-04-14 01:37:47.242463+04
29	catalog	0001_initial	2026-04-14 01:37:47.321489+04
30	cart	0001_initial	2026-04-14 01:37:47.377488+04
31	orders	0001_initial	2026-04-14 01:37:47.424661+04
32	repairs	0001_initial	2026-04-14 01:37:47.451107+04
33	sessions	0001_initial	2026-04-14 01:37:47.464839+04
34	sites	0001_initial	2026-04-14 01:37:47.471398+04
35	sites	0002_alter_domain_unique	2026-04-14 01:37:47.476018+04
36	socialaccount	0001_initial	2026-04-14 01:37:47.561065+04
37	socialaccount	0002_token_max_lengths	2026-04-14 01:37:47.588438+04
38	socialaccount	0003_extra_data_default_dict	2026-04-14 01:37:47.601192+04
39	socialaccount	0004_app_provider_id_settings	2026-04-14 01:37:47.631224+04
40	socialaccount	0005_socialtoken_nullable_app	2026-04-14 01:37:47.651371+04
41	socialaccount	0006_alter_socialaccount_extra_data	2026-04-14 01:37:47.673167+04
42	wishlist	0001_initial	2026-04-14 01:37:47.701255+04
43	catalog	0002_adbanner_image_file_category_image_file_productimage	2026-04-14 02:36:04.983504+04
44	catalog	0003_alter_category_options_and_more	2026-04-14 11:04:51.085763+04
45	catalog	0004_alter_setting_options_homepage	2026-04-19 01:32:37.737187+04
46	catalog	0005_adbanner_button_ar_adbanner_desc_ar_and_more	2026-04-19 23:42:07.244515+04
47	catalog	0006_stockmovement	2026-05-03 22:32:22.687635+04
48	orders	0002_order_bnpl_surcharge_order_region_order_shipping_fee_and_more	2026-05-03 23:27:47.44055+04
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
tvom3kz0ah5fllkbpi78vob1zi6p4b4m	e30:1wCP2x:b9dRNszj3Nx67M8HDmVtpOEAg9sqmObm13f2X_EVkyg	2026-04-28 01:42:19.501293+04
nqqbgdsll8irho98cqm6q8s4g40w5bvb	.eJxVjDsOwjAQBe_iGllefxNKes5grb1rHECOFCcV4u4QKQW0b2beS0Tc1hq3zkucSJyFFqffLWF-cNsB3bHdZpnnti5TkrsiD9rldSZ-Xg7376Bir9-aLRgmA5i5FFto8InYI43KWDWopIuHkE2BHAyOGoz3LpPTjiAoKCzeHwM5OCU:1wCXY2:4pb35ScAvPtAXSjjTxW8hqUmiZE-o4FXq72ye12Mrz0	2026-04-28 10:46:58.611279+04
ep3ao125r53y1r19ru4a9b4mu4x4dbtp	.eJxVjDsOwjAQBe_iGllefxNKes5grb1rHECOFCcV4u4QKQW0b2beS0Tc1hq3zkucSJyFFqffLWF-cNsB3bHdZpnnti5TkrsiD9rldSZ-Xg7376Bir9-aLRgmA5i5FFto8InYI43KWDWopIuHkE2BHAyOGoz3LpPTjiAoKCzeHwM5OCU:1wCXzI:M9_Xq3RkdzeMLJdd09_IU4oIGD3VmDJqbQzkxhBNGPc	2026-04-28 11:15:08.48139+04
3uhy9gpj3a6egdbx4nmb0ugos31y3zu4	.eJxVjDsOwjAQBe_iGllefxNKes5grb1rHECOFCcV4u4QKQW0b2beS0Tc1hq3zkucSJyFFqffLWF-cNsB3bHdZpnnti5TkrsiD9rldSZ-Xg7376Bir9-aLRgmA5i5FFto8InYI43KWDWopIuHkE2BHAyOGoz3LpPTjiAoKCzeHwM5OCU:1wCaFp:TcAvtPdLbAc3Xfl8lyEDXNLKIl25AFOPRc5SPvNrHKI	2026-04-28 13:40:21.936353+04
xc2cc1q7jw74h5ezd9or6nofnk46t3eq	.eJxVjDsOwjAQBe_iGllefxNKes5grb1rHECOFCcV4u4QKQW0b2beS0Tc1hq3zkucSJyFFqffLWF-cNsB3bHdZpnnti5TkrsiD9rldSZ-Xg7376Bir9-aLRgmA5i5FFto8InYI43KWDWopIuHkE2BHAyOGoz3LpPTjiAoKCzeHwM5OCU:1wEC06:EoPrfyR9q73vsTRo4U9_xOokPsjijydVfDSQGDZoK5s	2026-05-03 00:10:46.643394+04
la39emdls123601eelrnq6nrmnhtxi35	.eJxVjMEOwiAQRP-FsyEFqgWP3vsNZGF3pWogKe3J-O9C0oNeZjIzL_MWHvYt-b3S6hcUV2HE6bcLEJ-U-4APyPciY8nbugTZEXmsVc4F6XU72L-DBDX1W0eopzEqYxGB2SoHZ2xJj8w8agYdQCvmZpamOATHpK29UBhMU_H5AgIvOM0:1wHuB4:z-EIXlOSnZsjFaRnUBMfU11CzKFXNOjnaOCwLcL7slk	2026-05-13 05:57:26.78949+04
2n4f90b3knkt08jipjyk0urg97gre650	.eJxVjDsOwjAQBe_iGllefxNKes5grb1rHECOFCcV4u4QKQW0b2beS0Tc1hq3zkucSJyFFqffLWF-cNsB3bHdZpnnti5TkrsiD9rldSZ-Xg7376Bir9-aLRgmA5i5FFto8InYI43KWDWopIuHkE2BHAyOGoz3LpPTjiAoKCzeHwM5OCU:1wJbOh:gSu501LlLFv26QjaUrQGam-gzCv2KhtfapOVf84P8uw	2026-05-17 22:18:31.965692+04
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: orders_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders_order (id, reference, name, email, phone, address_line1, address_line2, city, postal_code, country, currency, subtotal, total, payment_method, provider, provider_ref, paid, status, referral_source, referral_other, line_items, created_at, updated_at, user_id, bnpl_surcharge, region, shipping_fee) FROM stdin;
9	0d788430-8c6a-4808-aeba-f17918430d38	Demo User	demo@shahzad.ae	+971501234567	Rolla Square, Al Wahda St		Sharjah	00000	UAE	AED	3699.00	3699.00	tamara	tamara		t	paid			[]	2026-04-29 05:44:39.102427+04	2026-04-29 05:44:39.102427+04	1	0.00	UAE	0.00
10	b66a9d00-943f-42a9-8702-4d1d43a656cf	Demo User	demo@shahzad.ae	+971501234567	Rolla Square, Al Wahda St		Sharjah	00000	UAE	AED	6198.00	6198.00	cod	cod		t	delivered			[]	2026-04-29 05:44:39.110724+04	2026-04-29 05:44:39.110724+04	1	0.00	UAE	0.00
11	de03c9e9-3173-4008-be9c-c9ea02a366f8	Demo User	demo@shahzad.ae	+971501234567	Rolla Square, Al Wahda St		Sharjah	00000	UAE	AED	7797.00	7797.00	tabby	tabby		t	shipped			[]	2026-04-29 05:44:39.11867+04	2026-04-29 05:44:39.11867+04	1	0.00	UAE	0.00
12	3913d63d-118a-4103-bfd9-7ef261ec3faa	Demo User	demo@shahzad.ae	+971501234567	Rolla Square, Al Wahda St		Sharjah	00000	UAE	AED	159.00	159.00	cod	cod		f	pending			[]	2026-04-29 05:44:39.127773+04	2026-04-29 05:44:39.127773+04	1	0.00	UAE	0.00
13	0a201f27-b185-4774-9c71-ac50fe366811	adib khan	ahmed.karim@example.ae	+971501234567	Rolla Square, Al Wahda St	Building 42, Apt 7	Sharjah	00000	UAE	AED	1.00	1.00	tamara	tamara	sandbox	f	pending			[{"quantity": 1, "price_data": {"currency": "aed", "unit_amount": 100, "product_data": {"name": "test product"}}}]	2026-05-03 23:01:11.704356+04	2026-05-03 23:01:11.704356+04	\N	0.00	UAE	0.00
14	ad2eb52c-749d-4588-98a7-e1d98bfa1758	Ahmed Karim	ahmed.karim@example.ae	+971501234567	Rolla Square, Al Wahda St	Building 42, Apt 7	Sharjah	00000	UAE	AED	1.00	31.00	cod	cod		f	pending			[{"quantity": 1, "price_data": {"currency": "aed", "unit_amount": 100, "product_data": {"name": "test product"}}}]	2026-05-04 00:11:52.8975+04	2026-05-04 00:11:52.8975+04	\N	0.00	UAE	30.00
15	564d246a-37f0-43bd-9b52-b16fc12b87ba	Ahmed Karim	ahmed.karim@example.ae	+971501234567	Rolla Square, Al Wahda St	Building 42, Apt 7	Sharjah	00000	UAE	AED	1.00	31.09	tamara	tamara	sandbox	f	pending			[{"quantity": 1, "price_data": {"currency": "aed", "unit_amount": 100, "product_data": {"name": "test product"}}}]	2026-05-04 00:13:53.318463+04	2026-05-04 00:13:53.318463+04	\N	0.09	UAE	30.00
17	e5f44801-bb2e-4db2-b58c-385971df1852	khanadib418	khanadib418@gmail.com	+971501234567	Rolla Square, Al Wahda St	Building 42, Apt 7	Sharjah	00000	UAE	AED	1.00	31.09	tamara	tamara	c9681334-6b7a-49cd-8d32-6fab4a15cb2c	f	cancelled			[{"quantity": 1, "price_data": {"currency": "aed", "unit_amount": 100, "product_data": {"name": "test product"}}}]	2026-05-04 00:27:51.820749+04	2026-05-04 00:28:19.403838+04	3	0.09	UAE	30.00
\.


--
-- Data for Name: orders_orderitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders_orderitem (id, title, unit_price, quantity, image, order_id, product_id) FROM stdin;
7	Samsung Galaxy S24+ 256GB Onyx Black	3699.00	1	https://images.unsplash.com/photo-1707412512271-ed99af1bd7ec?w=800	9	97
8	MacBook Air 15" M2 8GB / 256GB Starlight	4699.00	1	https://images.unsplash.com/photo-1639249227523-78502fbcfdc4?w=800	10	111
9	iPad 10th Gen 64GB Wi-Fi Silver	1499.00	1	https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800	10	107
10	iPhone 15 Pro Max 256GB Natural Titanium	4699.00	1	https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800	11	92
11	AirPods Max Space Gray	2299.00	1	https://images.unsplash.com/photo-1625948514430-3a3f56cd1e9c?w=800	11	117
12	AirPods 4 with Active Noise Cancellation	799.00	1	https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=800	11	118
13	Apple MagSafe Charger 1m	159.00	1	https://images.unsplash.com/photo-1625948514430-3a3f56cd1e9c?w=800	12	131
14	test product	1.00	1		13	139
15	test product	1.00	1		14	139
16	test product	1.00	1		15	139
18	test product	1.00	1		17	139
\.


--
-- Data for Name: repairs_repairbooking; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.repairs_repairbooking (id, reference, name, email, phone, device_brand, device_model, issue, preferred_drop_off, quoted_price, status, created_at, updated_at, service_id) FROM stdin;
6	2ae8074c-77a2-43c5-b90c-0a2dcfd927ce	Yousef Al Marzooqi	yousef@example.com	+971501234567	Apple	iPhone 14 Pro	Top-right corner cracked, touch unresponsive in that area. Dropped from waist height.	\N	299.00	ready	2026-04-29 05:44:39.129576+04	2026-04-29 05:44:39.129576+04	40
7	7b833bf0-c980-447b-96af-587b61859abf	Mariam Khalifa	mariam@example.com	+971502345678	Apple	iPhone 12	Battery health 78%, dies by mid-day. Phone is just over 2 years old.	\N	149.00	completed	2026-04-29 05:44:39.129576+04	2026-04-29 05:44:39.129576+04	42
8	5064dcbf-9978-406e-94bd-70e757832304	Ahmed Saif	ahmed@example.com	+971503456789	Apple	MacBook Air M2	Stepped on closed laptop. Bottom-left of screen cracked, top still works fine.	\N	899.00	in_progress	2026-04-29 05:44:39.129576+04	2026-04-29 05:44:39.129576+04	48
9	fca54b17-dc5b-46d9-9cc3-4ee1ec7784f0	Hessa Al Suwaidi	hessa@example.com	+971504567890	Dell	XPS 13 (2022)	Coffee spill on keyboard 24 hours ago. Won't power on. Important work files inside.	\N	349.00	quoted	2026-04-29 05:44:39.129576+04	2026-04-29 05:44:39.129576+04	51
10	b2f7a603-63ec-4f90-8122-ffe9671583c9	Tariq Hamdan	tariq@example.com	+971505678901	Samsung	Galaxy S23 Ultra	Long crack across the front. Phone still works, just want it fixed.	\N	\N	requested	2026-04-29 05:44:39.129576+04	2026-04-29 05:44:39.129576+04	41
\.


--
-- Data for Name: repairs_repairservice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.repairs_repairservice (id, name, slug, device, short_desc, description, base_price, est_minutes, icon, is_featured, "order") FROM stdin;
40	iPhone Screen Replacement	iphone-screen-replacement	phone	Genuine OLED display, lifetime labour warranty.	Apple-grade OLED panels for iPhone 8 through iPhone 15 Pro Max. Includes True Tone calibration, Face ID re-verification, and a lifetime labour warranty. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	299.00	45	📱	t	10
41	Android Screen Replacement	android-screen-replacement	phone	Samsung, Xiaomi, Pixel, OnePlus, Huawei, Honor.	Original Service Pack and OEM-grade replacement panels. AMOLED, OLED and LCD all supported. Full digitiser test before handover. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	249.00	45	📱	t	20
42	Phone Battery Replacement	phone-battery-replacement	phone	Restore full-day battery life. Same-day service.	We use only fresh-cell, 0-cycle batteries — never refurbished. Includes battery health calibration and a 6-month warranty. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	149.00	30	🔋	t	30
43	Charging Port Repair	charging-port-repair	phone	Fix slow charging, no detection, loose ports.	Lightning, USB-C and microUSB. Replacement of the entire charge-flex assembly when needed; ultrasonic clean if the port is just dirty. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	129.00	60	🔌	f	40
44	Water Damage Diagnosis	water-damage-diagnosis	phone	Free transparent quote before any work.	Ultrasonic motherboard cleaning, board-level component inspection, and data-recovery first. We give you a no-obligation quote before any repair. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	99.00	60	💧	f	50
45	Speaker / Microphone Repair	speaker-microphone-repair	phone	Get clear calls and audio back.	Earpiece, loudspeaker and microphone replacements. Often a quick fix after liquid exposure or accidental drops. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	139.00	45	🔊	f	60
46	Camera Module Replacement	camera-module-replacement	phone	Front and rear camera modules.	Cracked lens, blurry camera, no-detect issues. Front (selfie) or rear module replacement with full optical-image-stabilisation calibration. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	199.00	60	📸	f	70
47	Back Glass Replacement	back-glass-replacement	phone	Restore the back glass on iPhone & Samsung.	Laser-removed broken glass, then OEM-grade replacement back panel professionally adhesived. Wireless charging tested before return. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	229.00	90	🔁	f	80
48	Laptop Screen Replacement	laptop-screen-replacement	laptop	FHD, 4K and OLED panels for all major brands.	Apple, Dell, HP, Lenovo, ASUS, MSI. Touch and non-touch displays. We match your original panel resolution and refresh rate exactly. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	599.00	90	💻	t	100
49	Laptop Battery Replacement	laptop-battery-replacement	laptop	Genuine cells, 1-year warranty.	All major brands, including MacBook (Apple service-pack batteries) and ThinkPads. Includes battery calibration after install. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	349.00	45	🔋	f	110
50	Keyboard Replacement	keyboard-replacement	laptop	Sticky keys, dead keys, full keyboard swap.	Per-key replacement when possible, full keyboard assembly when not. Includes backlight ribbon if your model supports it. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	299.00	60	⌨️	f	120
51	Liquid Spill Recovery	liquid-spill-recovery	laptop	Ultrasonic motherboard cleaning, save your data.	Coffee, juice, or water — we strip down and ultrasonically clean every board. We always recover your data first when possible. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	249.00	120	💧	f	130
52	SSD Upgrade & Data Migration	ssd-upgrade-data-migration	laptop	New NVMe SSD up to 2TB + Windows clone.	Brand-name NVMe (Samsung, WD, Kingston). Includes full bit-by-bit clone of your old drive — boot back into your familiar setup. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	399.00	60	💾	f	140
53	RAM Upgrade	ram-upgrade	laptop	Boost performance — DDR4 / DDR5 modules.	We check compatibility, supply Crucial / Kingston / Samsung modules and stress-test the install. Soldered laptops can only upgrade if there's a spare slot — we'll tell you straight. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	199.00	30	🧠	f	150
54	Software / Virus Cleanup	software-virus-cleanup	laptop	Slow PC fix, virus removal, fresh Windows.	Full malware scan, junk-file purge, startup tuning. Fresh Windows install available — your files preserved. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	149.00	90	🛡️	f	160
55	Tablet Screen Replacement	tablet-screen-replacement	tablet	iPad, Galaxy Tab, and more.	Outer glass, full-display assembly, or digitiser-only — whichever your tablet needs. iPad Pro tandem-OLED replacements supported. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	499.00	90	📲	f	200
56	Tablet Battery Replacement	tablet-battery-replacement	tablet	Restore battery life on iPad and Galaxy Tab.	All-day battery returned. Includes battery-health calibration and a 1-year warranty on parts. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	299.00	90	🔋	f	210
57	Smart Watch Screen Replacement	smart-watch-screen-replacement	watch	Apple Watch, Galaxy Watch, Garmin.	Crystal, OLED display assembly, and digitiser replacements. Includes water-resistance reseal where the original gasket allows. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	399.00	90	⌚	f	300
58	Smart Watch Battery Replacement	smart-watch-battery-replacement	watch	Apple Watch and Galaxy Watch battery refresh.	Genuine-cell replacement, full battery health restored. Includes OS calibration and water-resistance reseal. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	249.00	60	🔋	f	310
59	Data Recovery	data-recovery	other	Recover photos, contacts, files from dead devices.	Phones, tablets, laptops, USB drives, microSD. Logical recovery (formatted / deleted) and physical recovery (broken board, dead drive). Quote varies by severity — we always tell you upfront. Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies.	299.00	240	🛟	f	400
\.


--
-- Data for Name: socialaccount_socialaccount; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.socialaccount_socialaccount (id, provider, uid, last_login, date_joined, extra_data, user_id) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialapp; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.socialaccount_socialapp (id, provider, name, client_id, secret, key, provider_id, settings) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialapp_sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.socialaccount_socialapp_sites (id, socialapp_id, site_id) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialtoken; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.socialaccount_socialtoken (id, token, token_secret, expires_at, account_id, app_id) FROM stdin;
\.


--
-- Data for Name: wishlist_wishedproduct; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wishlist_wishedproduct (id, added_at, product_id, user_id) FROM stdin;
\.


--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_emailaddress_id_seq', 1, false);


--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_emailconfirmation_id_seq', 1, false);


--
-- Name: accounts_address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_address_id_seq', 2, true);


--
-- Name: accounts_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_groups_id_seq', 1, false);


--
-- Name: accounts_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_id_seq', 4, true);


--
-- Name: accounts_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_user_permissions_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 120, true);


--
-- Name: cart_cart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_cart_id_seq', 27, true);


--
-- Name: cart_cartitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_cartitem_id_seq', 8, true);


--
-- Name: catalog_adbanner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_adbanner_id_seq', 35, true);


--
-- Name: catalog_brand_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_brand_id_seq', 84, true);


--
-- Name: catalog_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_category_id_seq', 25, true);


--
-- Name: catalog_homepage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_homepage_id_seq', 1, false);


--
-- Name: catalog_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_product_id_seq', 139, true);


--
-- Name: catalog_productimage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_productimage_id_seq', 1, false);


--
-- Name: catalog_qa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_qa_id_seq', 1, false);


--
-- Name: catalog_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_review_id_seq', 527, true);


--
-- Name: catalog_setting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_setting_id_seq', 1, false);


--
-- Name: catalog_stockmovement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.catalog_stockmovement_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 19, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 30, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 48, true);


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_order_id_seq', 17, true);


--
-- Name: orders_orderitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_orderitem_id_seq', 18, true);


--
-- Name: repairs_repairbooking_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.repairs_repairbooking_id_seq', 10, true);


--
-- Name: repairs_repairservice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.repairs_repairservice_id_seq', 59, true);


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.socialaccount_socialaccount_id_seq', 1, false);


--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.socialaccount_socialapp_id_seq', 1, false);


--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.socialaccount_socialapp_sites_id_seq', 1, false);


--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.socialaccount_socialtoken_id_seq', 1, false);


--
-- Name: wishlist_wishedproduct_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.wishlist_wishedproduct_id_seq', 17, true);


--
-- Name: account_emailaddress account_emailaddress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_pkey PRIMARY KEY (id);


--
-- Name: account_emailaddress account_emailaddress_user_id_email_987c8728_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_email_987c8728_uniq UNIQUE (user_id, email);


--
-- Name: account_emailconfirmation account_emailconfirmation_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_key_key UNIQUE (key);


--
-- Name: account_emailconfirmation account_emailconfirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_pkey PRIMARY KEY (id);


--
-- Name: accounts_address accounts_address_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_address
    ADD CONSTRAINT accounts_address_pkey PRIMARY KEY (id);


--
-- Name: accounts_user accounts_user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user
    ADD CONSTRAINT accounts_user_email_key UNIQUE (email);


--
-- Name: accounts_user_groups accounts_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_pkey PRIMARY KEY (id);


--
-- Name: accounts_user_groups accounts_user_groups_user_id_group_id_59c0b32f_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_user_id_group_id_59c0b32f_uniq UNIQUE (user_id, group_id);


--
-- Name: accounts_user accounts_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user
    ADD CONSTRAINT accounts_user_pkey PRIMARY KEY (id);


--
-- Name: accounts_user_user_permissions accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq UNIQUE (user_id, permission_id);


--
-- Name: accounts_user_user_permissions accounts_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: accounts_user accounts_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user
    ADD CONSTRAINT accounts_user_username_key UNIQUE (username);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: cart_cart cart_cart_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_cart
    ADD CONSTRAINT cart_cart_pkey PRIMARY KEY (id);


--
-- Name: cart_cart cart_cart_session_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_cart
    ADD CONSTRAINT cart_cart_session_key_key UNIQUE (session_key);


--
-- Name: cart_cart cart_cart_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_cart
    ADD CONSTRAINT cart_cart_user_id_key UNIQUE (user_id);


--
-- Name: cart_cartitem cart_cartitem_cart_id_product_id_53cce7c3_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_cartitem
    ADD CONSTRAINT cart_cartitem_cart_id_product_id_53cce7c3_uniq UNIQUE (cart_id, product_id);


--
-- Name: cart_cartitem cart_cartitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_cartitem
    ADD CONSTRAINT cart_cartitem_pkey PRIMARY KEY (id);


--
-- Name: catalog_adbanner catalog_adbanner_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_adbanner
    ADD CONSTRAINT catalog_adbanner_pkey PRIMARY KEY (id);


--
-- Name: catalog_brand catalog_brand_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_brand
    ADD CONSTRAINT catalog_brand_pkey PRIMARY KEY (id);


--
-- Name: catalog_brand catalog_brand_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_brand
    ADD CONSTRAINT catalog_brand_slug_key UNIQUE (slug);


--
-- Name: catalog_category catalog_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_category
    ADD CONSTRAINT catalog_category_pkey PRIMARY KEY (id);


--
-- Name: catalog_category catalog_category_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_category
    ADD CONSTRAINT catalog_category_slug_key UNIQUE (slug);


--
-- Name: catalog_homepage catalog_homepage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_homepage
    ADD CONSTRAINT catalog_homepage_pkey PRIMARY KEY (id);


--
-- Name: catalog_product catalog_product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_product
    ADD CONSTRAINT catalog_product_pkey PRIMARY KEY (id);


--
-- Name: catalog_product catalog_product_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_product
    ADD CONSTRAINT catalog_product_slug_key UNIQUE (slug);


--
-- Name: catalog_productimage catalog_productimage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_productimage
    ADD CONSTRAINT catalog_productimage_pkey PRIMARY KEY (id);


--
-- Name: catalog_qa catalog_qa_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_qa
    ADD CONSTRAINT catalog_qa_pkey PRIMARY KEY (id);


--
-- Name: catalog_review catalog_review_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_review
    ADD CONSTRAINT catalog_review_pkey PRIMARY KEY (id);


--
-- Name: catalog_setting catalog_setting_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_setting
    ADD CONSTRAINT catalog_setting_name_key UNIQUE (name);


--
-- Name: catalog_setting catalog_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_setting
    ADD CONSTRAINT catalog_setting_pkey PRIMARY KEY (id);


--
-- Name: catalog_stockmovement catalog_stockmovement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_stockmovement
    ADD CONSTRAINT catalog_stockmovement_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: orders_order orders_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_pkey PRIMARY KEY (id);


--
-- Name: orders_order orders_order_reference_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_reference_key UNIQUE (reference);


--
-- Name: orders_orderitem orders_orderitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_orderitem
    ADD CONSTRAINT orders_orderitem_pkey PRIMARY KEY (id);


--
-- Name: repairs_repairbooking repairs_repairbooking_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repairs_repairbooking
    ADD CONSTRAINT repairs_repairbooking_pkey PRIMARY KEY (id);


--
-- Name: repairs_repairbooking repairs_repairbooking_reference_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repairs_repairbooking
    ADD CONSTRAINT repairs_repairbooking_reference_key UNIQUE (reference);


--
-- Name: repairs_repairservice repairs_repairservice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repairs_repairservice
    ADD CONSTRAINT repairs_repairservice_pkey PRIMARY KEY (id);


--
-- Name: repairs_repairservice repairs_repairservice_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repairs_repairservice
    ADD CONSTRAINT repairs_repairservice_slug_key UNIQUE (slug);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_provider_uid_fc810c6e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_provider_uid_fc810c6e_uniq UNIQUE (provider, uid);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq UNIQUE (socialapp_id, site_id);


--
-- Name: socialaccount_socialapp socialaccount_socialapp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp
    ADD CONSTRAINT socialaccount_socialapp_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_sites_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq UNIQUE (app_id, account_id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_pkey PRIMARY KEY (id);


--
-- Name: catalog_brand unique_brand_per_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_brand
    ADD CONSTRAINT unique_brand_per_category UNIQUE (name, category_id);


--
-- Name: wishlist_wishedproduct wishlist_wishedproduct_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist_wishedproduct
    ADD CONSTRAINT wishlist_wishedproduct_pkey PRIMARY KEY (id);


--
-- Name: wishlist_wishedproduct wishlist_wishedproduct_user_id_product_id_338094c4_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist_wishedproduct
    ADD CONSTRAINT wishlist_wishedproduct_user_id_product_id_338094c4_uniq UNIQUE (user_id, product_id);


--
-- Name: account_emailaddress_email_03be32b2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX account_emailaddress_email_03be32b2 ON public.account_emailaddress USING btree (email);


--
-- Name: account_emailaddress_email_03be32b2_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX account_emailaddress_email_03be32b2_like ON public.account_emailaddress USING btree (email varchar_pattern_ops);


--
-- Name: account_emailaddress_user_id_2c513194; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX account_emailaddress_user_id_2c513194 ON public.account_emailaddress USING btree (user_id);


--
-- Name: account_emailconfirmation_email_address_id_5b7f8c58; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX account_emailconfirmation_email_address_id_5b7f8c58 ON public.account_emailconfirmation USING btree (email_address_id);


--
-- Name: account_emailconfirmation_key_f43612bd_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX account_emailconfirmation_key_f43612bd_like ON public.account_emailconfirmation USING btree (key varchar_pattern_ops);


--
-- Name: accounts_address_user_id_c8c74ddf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_address_user_id_c8c74ddf ON public.accounts_address USING btree (user_id);


--
-- Name: accounts_user_email_b2644a56_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_email_b2644a56_like ON public.accounts_user USING btree (email varchar_pattern_ops);


--
-- Name: accounts_user_groups_group_id_bd11a704; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_groups_group_id_bd11a704 ON public.accounts_user_groups USING btree (group_id);


--
-- Name: accounts_user_groups_user_id_52b62117; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_groups_user_id_52b62117 ON public.accounts_user_groups USING btree (user_id);


--
-- Name: accounts_user_user_permissions_permission_id_113bb443; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_user_permissions_permission_id_113bb443 ON public.accounts_user_user_permissions USING btree (permission_id);


--
-- Name: accounts_user_user_permissions_user_id_e4f0a161; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_user_permissions_user_id_e4f0a161 ON public.accounts_user_user_permissions USING btree (user_id);


--
-- Name: accounts_user_username_6088629e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_username_6088629e_like ON public.accounts_user USING btree (username varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: cart_cart_session_key_bf21cb35_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cart_cart_session_key_bf21cb35_like ON public.cart_cart USING btree (session_key varchar_pattern_ops);


--
-- Name: cart_cartitem_cart_id_370ad265; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cart_cartitem_cart_id_370ad265 ON public.cart_cartitem USING btree (cart_id);


--
-- Name: cart_cartitem_product_id_b24e265a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cart_cartitem_product_id_b24e265a ON public.cart_cartitem USING btree (product_id);


--
-- Name: catalog_brand_category_id_9bf3af96; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_brand_category_id_9bf3af96 ON public.catalog_brand USING btree (category_id);


--
-- Name: catalog_brand_slug_988c8dbc_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_brand_slug_988c8dbc_like ON public.catalog_brand USING btree (slug varchar_pattern_ops);


--
-- Name: catalog_category_parent_id_f61bd017; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_category_parent_id_f61bd017 ON public.catalog_category USING btree (parent_id);


--
-- Name: catalog_category_slug_dbf63ad0_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_category_slug_dbf63ad0_like ON public.catalog_category USING btree (slug varchar_pattern_ops);


--
-- Name: catalog_homepage_hero_product_id_594e8ad1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_homepage_hero_product_id_594e8ad1 ON public.catalog_homepage USING btree (hero_product_id);


--
-- Name: catalog_pro_is_acti_14fc6b_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_pro_is_acti_14fc6b_idx ON public.catalog_product USING btree (is_active);


--
-- Name: catalog_product_brand_409aa74f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_product_brand_409aa74f ON public.catalog_product USING btree (brand_id);


--
-- Name: catalog_product_category_id_35bf920b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_product_category_id_35bf920b ON public.catalog_product USING btree (category_id);


--
-- Name: catalog_product_slug_f37848b0_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_product_slug_f37848b0_like ON public.catalog_product USING btree (slug varchar_pattern_ops);


--
-- Name: catalog_productimage_product_id_1f42dd8c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_productimage_product_id_1f42dd8c ON public.catalog_productimage USING btree (product_id);


--
-- Name: catalog_qa_product_id_2f5761a3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_qa_product_id_2f5761a3 ON public.catalog_qa USING btree (product_id);


--
-- Name: catalog_review_product_id_e494243b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_review_product_id_e494243b ON public.catalog_review USING btree (product_id);


--
-- Name: catalog_setting_name_64ff6d39_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_setting_name_64ff6d39_like ON public.catalog_setting USING btree (name varchar_pattern_ops);


--
-- Name: catalog_stockmovement_product_id_13308dcf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_stockmovement_product_id_13308dcf ON public.catalog_stockmovement USING btree (product_id);


--
-- Name: catalog_stockmovement_user_id_fb907961; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX catalog_stockmovement_user_id_fb907961 ON public.catalog_stockmovement USING btree (user_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: orders_order_user_id_e9b59eb1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX orders_order_user_id_e9b59eb1 ON public.orders_order USING btree (user_id);


--
-- Name: orders_orderitem_order_id_fe61a34d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX orders_orderitem_order_id_fe61a34d ON public.orders_orderitem USING btree (order_id);


--
-- Name: orders_orderitem_product_id_afe4254a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX orders_orderitem_product_id_afe4254a ON public.orders_orderitem USING btree (product_id);


--
-- Name: repairs_repairbooking_service_id_65466e21; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX repairs_repairbooking_service_id_65466e21 ON public.repairs_repairbooking USING btree (service_id);


--
-- Name: repairs_repairservice_slug_e3338d11_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX repairs_repairservice_slug_e3338d11_like ON public.repairs_repairservice USING btree (slug varchar_pattern_ops);


--
-- Name: socialaccount_socialaccount_user_id_8146e70c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socialaccount_socialaccount_user_id_8146e70c ON public.socialaccount_socialaccount USING btree (user_id);


--
-- Name: socialaccount_socialapp_sites_site_id_2579dee5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socialaccount_socialapp_sites_site_id_2579dee5 ON public.socialaccount_socialapp_sites USING btree (site_id);


--
-- Name: socialaccount_socialapp_sites_socialapp_id_97fb6e7d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socialaccount_socialapp_sites_socialapp_id_97fb6e7d ON public.socialaccount_socialapp_sites USING btree (socialapp_id);


--
-- Name: socialaccount_socialtoken_account_id_951f210e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socialaccount_socialtoken_account_id_951f210e ON public.socialaccount_socialtoken USING btree (account_id);


--
-- Name: socialaccount_socialtoken_app_id_636a42d7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socialaccount_socialtoken_app_id_636a42d7 ON public.socialaccount_socialtoken USING btree (app_id);


--
-- Name: unique_primary_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX unique_primary_email ON public.account_emailaddress USING btree (user_id, "primary") WHERE "primary";


--
-- Name: unique_verified_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX unique_verified_email ON public.account_emailaddress USING btree (email) WHERE verified;


--
-- Name: wishlist_wishedproduct_product_id_4fbea32e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX wishlist_wishedproduct_product_id_4fbea32e ON public.wishlist_wishedproduct USING btree (product_id);


--
-- Name: wishlist_wishedproduct_user_id_1f294dea; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX wishlist_wishedproduct_user_id_1f294dea ON public.wishlist_wishedproduct USING btree (user_id);


--
-- Name: account_emailaddress account_emailaddress_user_id_2c513194_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_2c513194_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_emailconfirmation account_emailconfirm_email_address_id_5b7f8c58_fk_account_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirm_email_address_id_5b7f8c58_fk_account_e FOREIGN KEY (email_address_id) REFERENCES public.account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_address accounts_address_user_id_c8c74ddf_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_address
    ADD CONSTRAINT accounts_address_user_id_c8c74ddf_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_groups accounts_user_groups_group_id_bd11a704_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_group_id_bd11a704_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_groups accounts_user_groups_user_id_52b62117_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_user_id_52b62117_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_user_permissions accounts_user_user_p_permission_id_113bb443_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_p_permission_id_113bb443_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_user_permissions accounts_user_user_p_user_id_e4f0a161_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_p_user_id_e4f0a161_fk_accounts_ FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_cart cart_cart_user_id_9b4220b9_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_cart
    ADD CONSTRAINT cart_cart_user_id_9b4220b9_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_cartitem cart_cartitem_cart_id_370ad265_fk_cart_cart_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_cartitem
    ADD CONSTRAINT cart_cartitem_cart_id_370ad265_fk_cart_cart_id FOREIGN KEY (cart_id) REFERENCES public.cart_cart(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_cartitem cart_cartitem_product_id_b24e265a_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_cartitem
    ADD CONSTRAINT cart_cartitem_product_id_b24e265a_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_brand catalog_brand_category_id_9bf3af96_fk_catalog_category_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_brand
    ADD CONSTRAINT catalog_brand_category_id_9bf3af96_fk_catalog_category_id FOREIGN KEY (category_id) REFERENCES public.catalog_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_category catalog_category_parent_id_f61bd017_fk_catalog_category_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_category
    ADD CONSTRAINT catalog_category_parent_id_f61bd017_fk_catalog_category_id FOREIGN KEY (parent_id) REFERENCES public.catalog_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_homepage catalog_homepage_hero_product_id_594e8ad1_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_homepage
    ADD CONSTRAINT catalog_homepage_hero_product_id_594e8ad1_fk_catalog_product_id FOREIGN KEY (hero_product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_product catalog_product_brand_id_bb0c7890_fk_catalog_brand_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_product
    ADD CONSTRAINT catalog_product_brand_id_bb0c7890_fk_catalog_brand_id FOREIGN KEY (brand_id) REFERENCES public.catalog_brand(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_product catalog_product_category_id_35bf920b_fk_catalog_category_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_product
    ADD CONSTRAINT catalog_product_category_id_35bf920b_fk_catalog_category_id FOREIGN KEY (category_id) REFERENCES public.catalog_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_productimage catalog_productimage_product_id_1f42dd8c_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_productimage
    ADD CONSTRAINT catalog_productimage_product_id_1f42dd8c_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_qa catalog_qa_product_id_2f5761a3_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_qa
    ADD CONSTRAINT catalog_qa_product_id_2f5761a3_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_review catalog_review_product_id_e494243b_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_review
    ADD CONSTRAINT catalog_review_product_id_e494243b_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_stockmovement catalog_stockmovement_product_id_13308dcf_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_stockmovement
    ADD CONSTRAINT catalog_stockmovement_product_id_13308dcf_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_stockmovement catalog_stockmovement_user_id_fb907961_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalog_stockmovement
    ADD CONSTRAINT catalog_stockmovement_user_id_fb907961_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_order orders_order_user_id_e9b59eb1_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_user_id_e9b59eb1_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_orderitem orders_orderitem_order_id_fe61a34d_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_orderitem
    ADD CONSTRAINT orders_orderitem_order_id_fe61a34d_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_orderitem orders_orderitem_product_id_afe4254a_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_orderitem
    ADD CONSTRAINT orders_orderitem_product_id_afe4254a_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: repairs_repairbooking repairs_repairbookin_service_id_65466e21_fk_repairs_r; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repairs_repairbooking
    ADD CONSTRAINT repairs_repairbookin_service_id_65466e21_fk_repairs_r FOREIGN KEY (service_id) REFERENCES public.repairs_repairservice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_account_id_951f210e_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_account_id_951f210e_fk_socialacc FOREIGN KEY (account_id) REFERENCES public.socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_app_id_636a42d7_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_app_id_636a42d7_fk_socialacc FOREIGN KEY (app_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_social_site_id_2579dee5_fk_django_si; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_site_id_2579dee5_fk_django_si FOREIGN KEY (site_id) REFERENCES public.django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc FOREIGN KEY (socialapp_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialaccount socialaccount_social_user_id_8146e70c_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_social_user_id_8146e70c_fk_accounts_ FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: wishlist_wishedproduct wishlist_wishedprodu_product_id_4fbea32e_fk_catalog_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist_wishedproduct
    ADD CONSTRAINT wishlist_wishedprodu_product_id_4fbea32e_fk_catalog_p FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: wishlist_wishedproduct wishlist_wishedproduct_user_id_1f294dea_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist_wishedproduct
    ADD CONSTRAINT wishlist_wishedproduct_user_id_1f294dea_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

