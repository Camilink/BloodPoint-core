-- ==== BORRADO DE DATOS (orden correcto) ====
DELETE FROM authtoken_token;
DELETE FROM bloodpoint_app_donacion;
DELETE FROM bloodpoint_app_solicitud_campana_repo;
DELETE FROM bloodpoint_app_campana;
DELETE FROM bloodpoint_app_centro_donacion;
DELETE FROM bloodpoint_app_donante;
DELETE FROM bloodpoint_app_representante_org;
DELETE FROM bloodpoint_app_adminbp;
DELETE FROM bloodpoint_app_customuser;

-- ==== ADMINISTRADORES ====
INSERT INTO bloodpoint_app_customuser (
  email, password, tipo_usuario, is_staff, is_superuser, is_superadmin, is_active, date_joined, first_name, last_name
) VALUES
  ('admin@gmail.com', 'bloodpoint123', 'admin', TRUE, TRUE, TRUE, TRUE, CURRENT_TIMESTAMP, 'Juan', 'Pérez'),
  ('admin2@gmail.com', 'bloodpoint123', 'admin', TRUE, TRUE, TRUE, TRUE, CURRENT_TIMESTAMP, 'Carla', 'Soto'),
  ('admin3@gmail.com', 'bloodpoint123', 'admin', TRUE, TRUE, TRUE, TRUE, CURRENT_TIMESTAMP, 'María', 'Olivares');

INSERT INTO bloodpoint_app_adminbp (user_id, nombre, email, contrasena, created_at)
VALUES
  ((SELECT id FROM bloodpoint_app_customuser WHERE email = 'admin@gmail.com'), 'Juan Pérez', 'admin@gmail.com', 'bloodpoint123', CURRENT_TIMESTAMP),
  ((SELECT id FROM bloodpoint_app_customuser WHERE email = 'admin2@gmail.com'), 'Carla Soto', 'admin2@gmail.com', 'bloodpoint123', CURRENT_TIMESTAMP),
  ((SELECT id FROM bloodpoint_app_customuser WHERE email = 'admin3@gmail.com'), 'María Olivares', 'admin3@gmail.com', 'bloodpoint123', CURRENT_TIMESTAMP);

-- ==== REPRESENTANTES ====
INSERT INTO bloodpoint_app_customuser (
  email, password, tipo_usuario, first_name, last_name, is_active,
  is_superadmin, is_staff, is_superuser, date_joined
) VALUES
  ('camilaajojeda@gmail.com', 'bloodpoint123', 'representante', 'Camila', 'Jopia', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP),
  ('paulina678@gmail.com', 'bloodpoint123', 'representante', 'Paulina', 'Ríos', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP),
  ('cristian333@gmail.com', 'bloodpoint123', 'representante', 'Cristian', 'Morales', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP),
  ('lorena222@gmail.com', 'bloodpoint123', 'representante', 'Lorena', 'Silva', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP),
  ('matias999@gmail.com', 'bloodpoint123', 'representante', 'Matías', 'Figueroa', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP);

INSERT INTO bloodpoint_app_representante_org (
  user_id, rut_representante, rol, nombre, apellido, credencial, verificado, created_at
) VALUES
  ((SELECT id FROM bloodpoint_app_customuser WHERE email = 'camilaajojeda@gmail.com'), '17388920-5', 'Voluntaria Cruz Roja', 'Camila', 'Jopia', 'credencial1.pdf', TRUE, CURRENT_TIMESTAMP),
  ((SELECT id FROM bloodpoint_app_customuser WHERE email = 'paulina678@gmail.com'), '18845236-1', 'Representante institucional', 'Paulina', 'Ríos', 'credencial2.pdf', FALSE, CURRENT_TIMESTAMP),
  ((SELECT id FROM bloodpoint_app_customuser WHERE email = 'cristian333@gmail.com'), '16578431-9', 'Encargado logístico', 'Cristian', 'Morales', 'credencial3.pdf', TRUE, CURRENT_TIMESTAMP),
  ((SELECT id FROM bloodpoint_app_customuser WHERE email = 'lorena222@gmail.com'), '15793211-3', 'Representante institucional', 'Lorena', 'Silva', 'credencial4.pdf', TRUE, CURRENT_TIMESTAMP),
  ((SELECT id FROM bloodpoint_app_customuser WHERE email = 'matias999@gmail.com'), '17845622-5', 'Encargado logístico', 'Matías', 'Figueroa', 'credencial5.pdf', FALSE, CURRENT_TIMESTAMP);

-- ==== DONANTES ====
DO $$
DECLARE
  i INTEGER;
  nombres TEXT[] := ARRAY['Juan', 'Andrea', 'Roberto', 'Camila', 'Lucía', 'Felipe', 'María', 'Carlos', 'Sofía', 'Javier', 'Valentina', 'Pedro', 'Daniela', 'Tomás', 'Fernanda', 'Ignacio', 'Antonia', 'Diego', 'Martina', 'Benjamín', 'Josefa', 'Sebastián', 'Florencia', 'Vicente', 'Javiera', 'Agustín', 'Constanza', 'Matías', 'Trinidad', 'Andrés', 'Francisca', 'Leonardo', 'Catalina', 'Cristóbal', 'Paula'];
  apellidos TEXT[] := ARRAY['Araya', 'Castro', 'Mena', 'Herrera', 'Reyes', 'Gómez', 'Vera', 'López', 'Soto', 'Martínez', 'Ramírez', 'Rojas', 'Morales', 'Navarro', 'Gutiérrez', 'Salazar', 'Fuentes', 'Pizarro', 'Campos', 'Escobar', 'Alvarez', 'Peña', 'Carrasco', 'Silva', 'Muñoz', 'Torres', 'Orellana', 'Vargas', 'Ortega', 'Núñez', 'Zúñiga', 'Henríquez', 'Barrera', 'Sepúlveda', 'Palma'];
  tipo_sangres TEXT[] := ARRAY['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'];
  comunas TEXT[] := ARRAY['Providencia', 'Ñuñoa', 'Las Condes', 'Macul', 'San Miguel', 'La Florida', 'Puente Alto', 'Maipú', 'Recoleta', 'Santiago Centro'];
  dias TEXT[] := ARRAY['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'];
  rut_gen TEXT;
  correo TEXT;
BEGIN
  FOR i IN 1..35 LOOP
    rut_gen := '1' || i || '234567-' || (i % 9 + 1)::text;
    correo := LOWER(nombres[i]) || i || '@gmail.com';

    INSERT INTO bloodpoint_app_customuser (
      email, password, tipo_usuario, rut, first_name, last_name,
      is_active, is_superadmin, is_staff, is_superuser, date_joined
    ) VALUES (
      correo,
      'bloodpoint123',
      'donante',
      rut_gen,
      nombres[i],
      apellidos[i],
      TRUE,
      FALSE,
      FALSE,
      FALSE,
      CURRENT_TIMESTAMP
    );

    INSERT INTO bloodpoint_app_donante (
      user_id, rut, nombre_completo, sexo, ocupacion, direccion, comuna,
      fono, fecha_nacimiento, nacionalidad, tipo_sangre, dispo_dia_donacion,
      nuevo_donante, noti_emergencia, created_at
    ) VALUES (
      (SELECT id FROM bloodpoint_app_customuser WHERE email = correo),
      rut_gen,
      nombres[i] || ' ' || apellidos[i],
      CASE WHEN i % 2 = 0 THEN 'F' ELSE 'M' END,
      'Profesional Salud',
      'Calle Ficticia ' || i,
      comunas[(i % array_length(comunas, 1)) + 1],
      '+5691234' || LPAD(i::text, 4, '0'),
      '1990-01-01'::date + (i * 100),
      'Chilena',
      tipo_sangres[(i % array_length(tipo_sangres, 1)) + 1],
      dias[(i % array_length(dias, 1)) + 1],
      (i % 2 = 0),
      TRUE,
      CURRENT_TIMESTAMP
    );
  END LOOP;
END $$;
