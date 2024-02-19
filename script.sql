CREATE UNLOGGED TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY NOT NULL,
    limite INTEGER NOT NULL,
    saldo INTEGER NOT NULL
);

CREATE UNLOGGED TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY NOT NULL,
    tipo CHAR(1) NOT NULL,
    descricao VARCHAR(10) NOT NULL,
    valor INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    realizada_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cliente_id
ON transactions(cliente_id);

INSERT INTO clients (limite, saldo)
VALUES
    (100000, 0),
    (80000, 0),
    (1000000, 0),
    (10000000, 0),
    (500000, 0);

CREATE OR REPLACE FUNCTION update_balance()
RETURNS TRIGGER AS $$
DECLARE
    v_saldo INTEGER;
    v_limite INTEGER;
BEGIN
    SELECT saldo, limite INTO v_saldo, v_limite
    FROM clients WHERE id = NEW.cliente_id
    FOR UPDATE;

    IF NEW.tipo = 'd' AND (v_saldo - NEW.valor) < -v_limite THEN
        RAISE EXCEPTION USING
            errcode='23000',
            message='Limite insuficiente para realizar débito',
            hint='Realize um crédito para liberar mais limite';
    END IF;

    IF NEW.tipo = 'd' THEN
        UPDATE clients SET saldo = saldo - NEW.valor WHERE id = NEW.cliente_id;
    ELSE
        UPDATE clients SET saldo = saldo + NEW.valor WHERE id = NEW.cliente_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_balance_trigger
AFTER INSERT ON transactions
FOR EACH ROW
EXECUTE FUNCTION update_balance();

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;
