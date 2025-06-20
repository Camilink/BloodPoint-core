-- ----------------------------
-- 1. Limpiar tablas (DELETE) en orden para evitar violación de FK
-- ----------------------------
DELETE FROM bloodpoint_app_donacion;
DELETE FROM bloodpoint_app_campana;
DELETE FROM bloodpoint_app_solicitud_campana_repo;
DELETE FROM bloodpoint_app_centro_donacion;
DELETE FROM bloodpoint_app_representante_org;
DELETE FROM bloodpoint_app_customuser;

-- ----------------------------
-- 2. Insertar usuarios (CustomUser)
-- ----------------------------
INSERT INTO bloodpoint_app_customuser
(id, email, password, is_active, is_staff, is_superuser, tipo_usuario, username, date_joined)
VALUES
(1, 'rep1@example.com', 'hashedpassword1', TRUE, FALSE, FALSE, 'representante', 'rep1', NOW()),
(2, 'rep2@example.com', 'hashedpassword2', TRUE, FALSE, FALSE, 'representante', 'rep2', NOW()),
(3, 'rep3@example.com', 'hashedpassword3', TRUE, FALSE, FALSE, 'representante', 'rep3', NOW());

-- ----------------------------
-- 3. Insertar representantes_org
-- ----------------------------
INSERT INTO bloodpoint_app_representante_org
(id, telefono, nombre, apellido, id_usuario_id)
VALUES
(1, '912345678', 'Juan', 'Perez', 1),
(2, '987654321', 'Ana', 'Gonzalez', 2),
(3, '912398765', 'Luis', 'Rodriguez', 3);

-- ----------------------------
-- 4. Insertar centros de donación
-- ----------------------------
INSERT INTO bloodpoint_app_centro_donacion
(nombre_centro, direccion_centro, comuna, telefono, fecha_creacion, created_at, horario_apertura, horario_cierre, id_representante_id)
VALUES
('Centro Donación Santiago', 'Av. Libertador 123', 'Santiago', '22223333', '2020-01-10', NOW(), '08:00', '17:00', 1),
('Centro Donación Valparaíso', 'Calle Marina 456', 'Valparaíso', '22334455', '2020-02-15', NOW(), '09:00', '18:00', 2),
('Centro Donación Concepción', 'Paseo del Lago 789', 'Concepción', '22445566', '2020-03-20', NOW(), '07:30', '16:30', 3);

-- ----------------------------
-- 5. Insertar solicitudes de campaña
-- ----------------------------
INSERT INTO bloodpoint_app_solicitud_campana_repo
(tipo_sangre_sol, fecha_solicitud, cantidad_personas, descripcion_solicitud, comuna_solicitud, ciudad_solicitud, region_solicitud, created_at, fecha_termino, campana_asociada_id, centro_donacion_id, desactivado_por_id, id_donante_id)
VALUES
('A+', '2025-01-10', 10, 'Necesidad urgente de A+ en Santiago', 'Santiago', 'Santiago', 'Metropolitana', NOW(), '2025-01-30', NULL, 1, NULL, 1),
('B-', '2025-02-01', 8, 'Solicitud para pacientes con B-', 'Valparaíso', 'Valparaíso', 'Valparaíso', NOW(), '2025-02-20', NULL, 2, NULL, 2),
('O+', '2025-01-25', 12, 'Donación para emergencias O+', 'Concepción', 'Concepción', 'Biobío', NOW(), '2025-02-15', NULL, 3, NULL, 3),
('AB+', '2025-03-01', 5, 'Pacientes con AB+ requieren donaciones', 'Santiago', 'Santiago', 'Metropolitana', NOW(), '2025-03-20', NULL, 1, NULL, 1),
('O-', '2025-04-01', 7, 'Urgente sangre O- para quirófano', 'Valparaíso', 'Valparaíso', 'Valparaíso', NOW(), '2025-04-25', NULL, 2, NULL, 2);

-- ----------------------------
-- 6. Insertar campañas
-- ----------------------------
INSERT INTO bloodpoint_app_campana
(fecha_campana, apertura, cierre, meta, latitud, longitud, created_at, fecha_termino, validada, estado, id_centro_id, id_representante_id, id_solicitud_id, nombre_campana)
VALUES
('2025-01-15', '08:00', '18:00', '100 donantes',  -33, -70, NOW(), '2025-01-31', TRUE, 'activa', 1, 1, NULL, 'Campaña Santiago Enero'),
('2025-03-05', '09:00', '17:00', '80 donantes', -33, -71, NOW(), '2025-03-20', TRUE, 'activa', 1, 2, NULL, 'Campaña Valparaíso Marzo'),
('2025-02-10', '07:30', '16:30', '120 donantes', -36, -73, NOW(), '2025-02-28', TRUE, 'finalizada', 2, 3, NULL, 'Campaña Concepción Febrero'),
('2025-01-25', '08:00', '17:00', '90 donantes', -33, -70, NOW(), '2025-02-15', TRUE, 'activa', 3, 1, NULL, 'Campaña Santiago Febrero'),
('2025-04-15', '09:00', '18:00', '110 donantes', -36, -72, NOW(), '2025-04-30', TRUE, 'activa', 2, 2, NULL, 'Campaña Valparaíso Abril');

-- ----------------------------
-- 7. Insertar donaciones
-- ----------------------------
INSERT INTO bloodpoint_app_donacion
(fecha_donacion, cantidad_donacion, created_at, tipo_donacion, campana_relacionada_id, centro_id_id, id_donante_id, solicitud_relacionada_id, es_intencion, validada)
VALUES
-- Donaciones relacionadas con campañas
('2025-01-16', 1, NOW(), 'campaña', 1, 1, 1, NULL, FALSE, TRUE),
('2025-01-17', 1, NOW(), 'campaña', 1, 1, 2, NULL, FALSE, TRUE),
('2025-01-18', 1, NOW(), 'campaña', 1, 1, 3, NULL, FALSE, TRUE),
('2025-01-19', 1, NOW(), 'campaña', 1, 1, 4, NULL, FALSE, TRUE),
('2025-01-20', 1, NOW(), 'campaña', 1, 1, 5, NULL, FALSE, TRUE),

('2025-03-06', 1, NOW(), 'campaña', 2, 1, 6, NULL, FALSE, TRUE),
('2025-03-07', 1, NOW(), 'campaña', 2, 1, 7, NULL, FALSE, TRUE),

-- Donaciones relacionadas con solicitudes
('2025-05-01', 1, NOW(), 'solicitud', NULL, 1, 1, 1, TRUE, FALSE),
('2025-05-02', 1, NOW(), 'solicitud', NULL, 1, 2, 2, TRUE, FALSE),
('2025-05-03', 1, NOW(), 'solicitud', NULL, 2, 3, 3, TRUE, FALSE),
('2025-05-04', 1, NOW(), 'solicitud', NULL, 2, 4, 4, TRUE, FALSE);

