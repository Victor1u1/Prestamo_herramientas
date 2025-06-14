from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from herramientas.models import Herramienta
from prestamos.models import Prestamo
from calificaciones.models import Calificacion
import datetime
import random
# Añadir esta importación al inicio del archivo
import os
from django.conf import settings
from django.core.files.base import ContentFile
import requests
from io import BytesIO


Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Configura datos iniciales completos del sistema con estados variados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('🗑️  Eliminando datos existentes...')
            self.reset_data()
        
        self.stdout.write('🚀 Iniciando configuración de datos completos...')
        
        try:
            # 1. Crear usuarios
            usuarios = self.crear_usuarios()
            
            # 2. Crear herramientas
            herramientas = self.crear_herramientas(usuarios)
            
            # 3. Crear préstamos con estados variados
            prestamos = self.crear_prestamos(usuarios, herramientas)
            
            # 4. Crear calificaciones
            self.crear_calificaciones(prestamos)
            
            self.stdout.write(
                self.style.SUCCESS('✅ Configuración completada exitosamente!')
            )
            self.mostrar_resumen()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error durante la configuración: {e}')
            )

    def reset_data(self):
        """Elimina todos los datos existentes"""
        try:
            with transaction.atomic():
                # Eliminar en orden correcto para evitar problemas de FK
                Calificacion.objects.all().delete()
                self.stdout.write('  - Calificaciones eliminadas')
                
                Prestamo.objects.all().delete()
                self.stdout.write('  - Préstamos eliminados')
                
                Herramienta.objects.all().delete()
                self.stdout.write('  - Herramientas eliminadas')
                
                # Eliminar usuarios excepto superusuarios existentes
                Usuario.objects.filter(is_superuser=False).delete()
                self.stdout.write('  - Usuarios eliminados')
                
            self.stdout.write('✅ Datos eliminados correctamente')
        except Exception as e:
            self.stdout.write(f'❌ Error al eliminar datos: {e}')

    def crear_usuarios(self):
        """Crea usuarios con diferentes roles"""
        self.stdout.write('👥 Creando usuarios...')
        
        usuarios = []
        
        # Crear o actualizar superusuario admin
        try:
            with transaction.atomic():
                admin, created = Usuario.objects.get_or_create(
                    username='admin',
                    defaults={
                        'email': 'admin@example.com',
                        'first_name': 'Administrador',
                        'last_name': 'Sistema',
                        'direccion': 'Oficina Central 123',
                        'telefono': '555-0000',
                        'rol': 'admin',
                        'is_admin': True,
                        'is_staff': True,
                        'is_superuser': True
                    }
                )
                
                if created:
                    admin.set_password('admin123')
                    admin.save()
                    self.stdout.write(f"✅ Superusuario creado: {admin.username}")
                else:
                    # Actualizar usuario existente
                    admin.email = 'admin@example.com'
                    admin.first_name = 'Administrador'
                    admin.last_name = 'Sistema'
                    admin.direccion = 'Oficina Central 123'
                    admin.telefono = '555-0000'
                    admin.rol = 'admin'
                    admin.is_admin = True
                    admin.is_staff = True
                    admin.is_superuser = True
                    admin.set_password('admin123')
                    admin.save()
                    self.stdout.write(f"✅ Superusuario actualizado: {admin.username}")
                    
        except Exception as e:
            self.stdout.write(f"❌ Error al crear/actualizar admin: {e}")
        
        # Datos de usuarios vecinos (más usuarios para más variedad)
        usuarios_data = [
            {
                'username': 'carlos_martinez',
                'email': 'carlos@email.com',
                'first_name': 'Carlos',
                'last_name': 'Martínez',
                'direccion': 'Calle Principal 123',
                'telefono': '555-1001'
            },
            {
                'username': 'ana_rodriguez',
                'email': 'ana@email.com',
                'first_name': 'Ana',
                'last_name': 'Rodríguez',
                'direccion': 'Avenida Central 456',
                'telefono': '555-1002'
            },
            {
                'username': 'miguel_lopez',
                'email': 'miguel@email.com',
                'first_name': 'Miguel',
                'last_name': 'López',
                'direccion': 'Plaza Mayor 789',
                'telefono': '555-1003'
            },
            {
                'username': 'sofia_garcia',
                'email': 'sofia@email.com',
                'first_name': 'Sofía',
                'last_name': 'García',
                'direccion': 'Barrio Norte 321',
                'telefono': '555-1004'
            },
            {
                'username': 'pedro_sanchez',
                'email': 'pedro@email.com',
                'first_name': 'Pedro',
                'last_name': 'Sánchez',
                'direccion': 'Zona Sur 654',
                'telefono': '555-1005'
            },
            {
                'username': 'lucia_fernandez',
                'email': 'lucia@email.com',
                'first_name': 'Lucía',
                'last_name': 'Fernández',
                'direccion': 'Sector Este 987',
                'telefono': '555-1006'
            },
            {
                'username': 'david_torres',
                'email': 'david@email.com',
                'first_name': 'David',
                'last_name': 'Torres',
                'direccion': 'Colonia Oeste 147',
                'telefono': '555-1007'
            },
            {
                'username': 'maria_jimenez',
                'email': 'maria@email.com',
                'first_name': 'María',
                'last_name': 'Jiménez',
                'direccion': 'Residencial Centro 258',
                'telefono': '555-1008'
            },
            {
                'username': 'roberto_morales',
                'email': 'roberto@email.com',
                'first_name': 'Roberto',
                'last_name': 'Morales',
                'direccion': 'Urbanización Nueva 369',
                'telefono': '555-1009'
            },
            {
                'username': 'elena_vargas',
                'email': 'elena@email.com',
                'first_name': 'Elena',
                'last_name': 'Vargas',
                'direccion': 'Conjunto Residencial 741',
                'telefono': '555-1010'
            },
            {
                'username': 'fernando_castro',
                'email': 'fernando@email.com',
                'first_name': 'Fernando',
                'last_name': 'Castro',
                'direccion': 'Barrio Antiguo 852',
                'telefono': '555-1011'
            },
            {
                'username': 'patricia_ruiz',
                'email': 'patricia@email.com',
                'first_name': 'Patricia',
                'last_name': 'Ruiz',
                'direccion': 'Sector Comercial 963',
                'telefono': '555-1012'
            },
            {
                'username': 'alejandro_herrera',
                'email': 'alejandro@email.com',
                'first_name': 'Alejandro',
                'last_name': 'Herrera',
                'direccion': 'Zona Industrial 159',
                'telefono': '555-1013'
            },
            {
                'username': 'carmen_mendoza',
                'email': 'carmen@email.com',
                'first_name': 'Carmen',
                'last_name': 'Mendoza',
                'direccion': 'Colonia Moderna 357',
                'telefono': '555-1014'
            },
            {
                'username': 'javier_ortega',
                'email': 'javier@email.com',
                'first_name': 'Javier',
                'last_name': 'Ortega',
                'direccion': 'Fraccionamiento Los Pinos 468',
                'telefono': '555-1015'
            }
        ]
        
        for data in usuarios_data:
            try:
                with transaction.atomic():
                    usuario, created = Usuario.objects.get_or_create(
                        username=data['username'],
                        defaults={
                            'email': data['email'],
                            'first_name': data['first_name'],
                            'last_name': data['last_name'],
                            'direccion': data['direccion'],
                            'telefono': data['telefono'],
                            'rol': 'vecino'
                        }
                    )
                    
                    if created:
                        usuario.set_password('123456')  # Contraseña más simple
                        usuario.save()
                        self.stdout.write(f"✅ Usuario creado: {usuario.username}")
                    else:
                        # Actualizar datos si el usuario ya existe
                        usuario.email = data['email']
                        usuario.first_name = data['first_name']
                        usuario.last_name = data['last_name']
                        usuario.direccion = data['direccion']
                        usuario.telefono = data['telefono']
                        usuario.rol = 'vecino'
                        usuario.set_password('123456')
                        usuario.save()
                        self.stdout.write(f"✅ Usuario actualizado: {usuario.username}")
                    
                    usuarios.append(usuario)
                    
            except Exception as e:
                self.stdout.write(f"❌ Error al crear usuario {data['username']}: {e}")
        
        return usuarios

    def crear_herramientas(self, usuarios):
        """Crea herramientas con diferentes estados y disponibilidades"""
        self.stdout.write('🔧 Creando herramientas...')
        
        # URLs de imágenes de ejemplo para herramientas
        imagenes_ejemplo = [
            "https://m.media-amazon.com/images/I/71aXLDooQqL._AC_SL1500_.jpg",  # Taladro
            "https://m.media-amazon.com/images/I/71Qcf7LvHYL._AC_SL1500_.jpg",  # Sierra circular
            "https://m.media-amazon.com/images/I/71rlNs38FoL._AC_SL1500_.jpg",  # Lijadora
            "https://m.media-amazon.com/images/I/71jzfN2IQTL._AC_SL1500_.jpg",  # Martillo
            "https://m.media-amazon.com/images/I/61Yl0OwSvOL._AC_SL1500_.jpg",  # Destornillador
            "https://m.media-amazon.com/images/I/71Jdl4HTnUL._AC_SL1500_.jpg",  # Podadora
            "https://m.media-amazon.com/images/I/71Kkm5OQsIL._AC_SL1500_.jpg",  # Cortacésped
            "https://m.media-amazon.com/images/I/71KI2H7vXVL._AC_SL1500_.jpg",  # Motosierra
            "https://m.media-amazon.com/images/I/71Hs+ZV4XVL._AC_SL1500_.jpg",  # Sopladora
            "https://m.media-amazon.com/images/I/71Hs+ZV4XVL._AC_SL1500_.jpg",  # Bordeadora
        ]
        
        herramientas_data = [
            # Herramientas de construcción y carpintería
            {'nombre': 'Taladro Bosch Professional GSB 18V', 'descripcion': 'Taladro atornillador inalámbrico de 18V con percutor, incluye 2 baterías, cargador y maletín con brocas', 'estado': 'nuevo', 'disponibilidad': 'disponible'},
            {'nombre': 'Sierra Circular Makita 5007MG', 'descripcion': 'Sierra circular de 1800W con disco de 7 1/4", guía láser y base de magnesio para cortes precisos', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Lijadora Orbital Black & Decker KA280', 'descripcion': 'Lijadora orbital de 240W con sistema de aspiración de polvo y base perforada', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Martillo Demoledor Hilti TE 30', 'descripcion': 'Martillo neumático para demolición de 850W, incluye cinceles y puntas variadas', 'estado': 'regular', 'disponibilidad': 'mantenimiento'},
            {'nombre': 'Destornillador Inalámbrico DeWalt DCD771C2', 'descripcion': 'Destornillador inalámbrico de 20V MAX con batería de litio y cargador rápido', 'estado': 'nuevo', 'disponibilidad': 'disponible'},
            
            # Herramientas de jardín
            {'nombre': 'Podadora Eléctrica Ryobi RLM18X33S40', 'descripcion': 'Podadora eléctrica de césped de 1800W con cesta recolectora de 50L y altura ajustable', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Cortacésped Honda HRX217VKA', 'descripcion': 'Cortacésped a gasolina autopropulsado, motor 4 tiempos de 190cc con sistema de mulching', 'estado': 'bueno', 'disponibilidad': 'prestada'},
            {'nombre': 'Motosierra Stihl MS 250', 'descripcion': 'Motosierra profesional de 16 pulgadas para poda y corte, motor de 2 tiempos', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Sopladora de Hojas Echo PB-2520', 'descripcion': 'Sopladora de hojas a gasolina de mochila, motor de 2 tiempos de 25.4cc', 'estado': 'regular', 'disponibilidad': 'disponible'},
            {'nombre': 'Bordeadora Eléctrica Worx WG163', 'descripcion': 'Bordeadora eléctrica de 12 pulgadas con cabezal giratorio y ruedas guía', 'estado': 'nuevo', 'disponibilidad': 'disponible'},
            
            # Resto de herramientas...
            # Herramientas especializadas
            {'nombre': 'Soldadora Inverter Lincoln Electric', 'descripcion': 'Soldadora eléctrica inverter de 200A con tecnología IGBT, incluye electrodos y careta', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Compresor de Aire Stanley D200/10/24', 'descripcion': 'Compresor de aire de 24 litros con pistola de pintura y accesorios neumáticos', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Pulidora Angular Bosch GWS 22-230 JH', 'descripcion': 'Pulidora angular de 2200W con discos de corte y pulido, empuñadura antivibración', 'estado': 'nuevo', 'disponibilidad': 'disponible'},
            {'nombre': 'Hidrolavadora Kärcher K5 Premium', 'descripcion': 'Hidrolavadora de alta presión 145 bar con manguera de 8m y boquillas intercambiables', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Generador Eléctrico Honda EU3000iS', 'descripcion': 'Generador eléctrico portátil de 3000W, motor a gasolina con tecnología inverter', 'estado': 'bueno', 'disponibilidad': 'inactiva'},
            
            # Herramientas de medición y precisión
            {'nombre': 'Taladro de Columna Craftsman 12"', 'descripcion': 'Taladro de columna de mesa, motor de 500W con mesa ajustable y precisión profesional', 'estado': 'regular', 'disponibilidad': 'disponible'},
            {'nombre': 'Nivel Láser Bosch GLL 3-80', 'descripcion': 'Nivel láser de líneas cruzadas con alcance de 30m y base magnética', 'estado': 'nuevo', 'disponibilidad': 'disponible'},
            {'nombre': 'Medidor de Distancia Láser Leica DISTO D2', 'descripcion': 'Medidor de distancia láser con precisión de ±1.5mm y alcance de 100m', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            
            # Herramientas de limpieza
            {'nombre': 'Aspiradora Industrial Kärcher WD 6 P Premium', 'descripcion': 'Aspiradora industrial para sólidos y líquidos de 30 litros con filtro HEPA', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Pistola de Calor Black & Decker KX2200K', 'descripcion': 'Pistola de calor de 2000W con control de temperatura y boquillas intercambiables', 'estado': 'nuevo', 'disponibilidad': 'disponible'},
            {'nombre': 'Pulidora de Pisos Oreck Commercial ORB550MC', 'descripcion': 'Pulidora de pisos comercial con almohadillas y sistema de aspersión', 'estado': 'regular', 'disponibilidad': 'disponible'},
            
            # Herramientas adicionales
            {'nombre': 'Escalera Telescópica Little Giant', 'descripcion': 'Escalera telescópica de aluminio multiposición, alcance hasta 4.5 metros', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Carretilla de Construcción Truper', 'descripcion': 'Carretilla de construcción de 90 litros con llanta neumática y estructura reforzada', 'estado': 'regular', 'disponibilidad': 'disponible'},
            {'nombre': 'Gato Hidráulico de Piso 3 Toneladas', 'descripcion': 'Gato hidráulico de piso para automóviles con capacidad de 3 toneladas', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Esmeriladora de Banco Craftsman 8"', 'descripcion': 'Esmeriladora de banco de 8 pulgadas con motor de 3/4 HP y luces LED', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Sierra de Mesa DeWalt DWE7491RS', 'descripcion': 'Sierra de mesa portátil de 10" con soporte rodante y sistema de seguridad', 'estado': 'nuevo', 'disponibilidad': 'disponible'},
            {'nombre': 'Rotomartillo Makita HR2475', 'descripcion': 'Rotomartillo SDS-Plus de 780W con 3 funciones: taladrar, martillar y cincelar', 'estado': 'bueno', 'disponibilidad': 'prestada'},
            {'nombre': 'Pistola de Clavos Neumática Bostitch N62FNK-2', 'descripcion': 'Pistola de clavos neumática para acabados con clavos de 15 a 64mm', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Vibrador de Concreto Enar DINGO', 'descripcion': 'Vibrador de concreto eléctrico con manguera flexible de 4 metros', 'estado': 'regular', 'disponibilidad': 'disponible'},
            {'nombre': 'Mezcladora de Concreto 140L', 'descripcion': 'Mezcladora de concreto eléctrica de 140 litros con motor de 1HP', 'estado': 'bueno', 'disponibilidad': 'disponible'},
            {'nombre': 'Cortadora de Azulejo Rubi TX-900N', 'descripcion': 'Cortadora de azulejo eléctrica con disco diamantado y sistema de refrigeración', 'estado': 'nuevo', 'disponibilidad': 'disponible'},
        ]
        
        # Asegurarse de que existe el directorio para las imágenes
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'herramientas'), exist_ok=True)
        
        herramientas = []
        for i, data in enumerate(herramientas_data):
            if i < len(usuarios):
                propietario = usuarios[i % len(usuarios)]
                try:
                    with transaction.atomic():
                        herramienta, created = Herramienta.objects.get_or_create(
                            nombre=data['nombre'],
                            propietario=propietario,
                            defaults={
                                'descripcion': data['descripcion'],
                                'estado': data['estado'],
                                'disponibilidad': data['disponibilidad']
                            }
                        )
                        
                        # Intentar descargar y asignar una imagen si la herramienta es nueva
                        if created and i < len(imagenes_ejemplo):
                            try:
                                # Descargar imagen
                                response = requests.get(imagenes_ejemplo[i % len(imagenes_ejemplo)])
                                if response.status_code == 200:
                                    # Crear nombre de archivo único con timestamp
                                    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
                                    img_name = f"{herramienta.nombre.replace(' ', '_').lower()}_{timestamp}.jpg"
                                    # Guardar imagen
                                    herramienta.imagen.save(img_name, ContentFile(response.content), save=True)
                                    self.stdout.write(f"✅ Imagen asignada a: {herramienta.nombre}")
                            except Exception as e:
                                self.stdout.write(f"❌ Error al descargar imagen para {herramienta.nombre}: {e}")
                        
                        herramientas.append(herramienta)
                        if created:
                            self.stdout.write(f"✅ Herramienta creada: {herramienta.nombre} (Propietario: {propietario.username})")
                        else:
                            self.stdout.write(f"✅ Herramienta existente: {herramienta.nombre}")
                except Exception as e:
                    self.stdout.write(f"❌ Error al crear herramienta {data['nombre']}: {e}")
        
        return herramientas

    def crear_prestamos(self, usuarios, herramientas):
        """Crea préstamos variados para todos los usuarios"""
        self.stdout.write('📋 Creando préstamos variados...')
        
        prestamos = []
        estados_disponibles = ['pendiente', 'aceptado', 'rechazado', 'en_curso', 'finalizado', 'cancelado']
        
        # Crear múltiples préstamos para cada usuario
        for usuario in usuarios:
            # Cada usuario tendrá entre 2 y 5 préstamos
            num_prestamos = random.randint(2, 5)
            
            for _ in range(num_prestamos):
                try:
                    # Seleccionar una herramienta aleatoria que no sea del mismo usuario
                    herramientas_disponibles = [h for h in herramientas if h.propietario != usuario]
                    
                    if herramientas_disponibles:
                        herramienta = random.choice(herramientas_disponibles)
                        
                        # Generar fechas aleatorias
                        dias_inicio = random.randint(-30, 10)  # Desde hace 30 días hasta 10 días en el futuro
                        dias_duracion = random.randint(1, 7)   # Duración de 1 a 7 días
                        
                        fecha_inicio = timezone.now().date() + datetime.timedelta(days=dias_inicio)
                        fecha_fin = fecha_inicio + datetime.timedelta(days=dias_duracion)
                        
                        # Seleccionar estado basado en las fechas
                        if dias_inicio > 0:  # Préstamos futuros
                            estado = random.choice(['pendiente', 'aceptado'])
                        elif dias_inicio <= 0 and (fecha_fin >= timezone.now().date()):  # Préstamos actuales
                            estado = random.choice(['en_curso', 'aceptado'])
                        else:  # Préstamos pasados
                            estado = random.choice(['finalizado', 'cancelado', 'rechazado'])
                        
                        with transaction.atomic():
                            # Verificar que no existe ya un préstamo igual
                            prestamo_existente = Prestamo.objects.filter(
                                herramienta=herramienta,
                                prestatario=usuario,
                                fecha_inicio=fecha_inicio
                            ).first()
                            
                            if not prestamo_existente:
                                prestamo = Prestamo.objects.create(
                                    herramienta=herramienta,
                                    prestatario=usuario,
                                    fecha_inicio=fecha_inicio,
                                    fecha_fin=fecha_fin,
                                    estado=estado
                                )
                                prestamos.append(prestamo)
                                self.stdout.write(f"✅ Préstamo creado: {herramienta.nombre} -> {usuario.username} ({estado})")
                            
                except Exception as e:
                    self.stdout.write(f"❌ Error al crear préstamo para {usuario.username}: {e}")
        
        # Crear algunos préstamos adicionales específicos para demostrar funcionalidades
        prestamos_especificos = [
            # Préstamos pendientes para probar aprobación
            {'herramienta_idx': 0, 'usuario_idx': 5, 'dias_inicio': 1, 'dias_duracion': 3, 'estado': 'pendiente'},
            {'herramienta_idx': 2, 'usuario_idx': 7, 'dias_inicio': 2, 'dias_duracion': 4, 'estado': 'pendiente'},
            {'herramienta_idx': 4, 'usuario_idx': 9, 'dias_inicio': 0, 'dias_duracion': 2, 'estado': 'pendiente'},
            
            # Préstamos aceptados listos para iniciar
            {'herramienta_idx': 6, 'usuario_idx': 1, 'dias_inicio': 0, 'dias_duracion': 5, 'estado': 'aceptado'},
            {'herramienta_idx': 8, 'usuario_idx': 3, 'dias_inicio': 1, 'dias_duracion': 3, 'estado': 'aceptado'},
            
            # Préstamos en curso
            {'herramienta_idx': 10, 'usuario_idx': 2, 'dias_inicio': -2, 'dias_duracion': 6, 'estado': 'en_curso'},
            {'herramienta_idx': 12, 'usuario_idx': 4, 'dias_inicio': -1, 'dias_duracion': 4, 'estado': 'en_curso'},
        ]
        
        for data in prestamos_especificos:
            try:
                if (data['herramienta_idx'] < len(herramientas) and 
                    data['usuario_idx'] < len(usuarios)):
                    
                    herramienta = herramientas[data['herramienta_idx']]
                    usuario = usuarios[data['usuario_idx']]
                    
                    # Verificar que no sea el propietario
                    if herramienta.propietario != usuario:
                        fecha_inicio = timezone.now().date() + datetime.timedelta(days=data['dias_inicio'])
                        fecha_fin = fecha_inicio + datetime.timedelta(days=data['dias_duracion'])
                        
                        with transaction.atomic():
                            prestamo, created = Prestamo.objects.get_or_create(
                                herramienta=herramienta,
                                prestatario=usuario,
                                fecha_inicio=fecha_inicio,
                                defaults={
                                    'fecha_fin': fecha_fin,
                                    'estado': data['estado']
                                }
                            )
                            
                            if created:
                                prestamos.append(prestamo)
                                self.stdout.write(f"✅ Préstamo específico creado: {herramienta.nombre} -> {usuario.username} ({data['estado']})")
                            
            except Exception as e:
                self.stdout.write(f"❌ Error al crear préstamo específico: {e}")
        
        return prestamos

    def crear_calificaciones(self, prestamos):
        """Crea calificaciones para préstamos finalizados"""
        self.stdout.write('⭐ Creando calificaciones...')
        
        # Filtrar solo préstamos finalizados
        prestamos_finalizados = [p for p in prestamos if p.estado == 'finalizado']
        
        comentarios_positivos = [
            'Excelente herramienta, muy bien cuidada. El propietario fue muy amable y flexible con los horarios.',
            'Herramienta en perfecto estado, exactamente lo que necesitaba. Muy buen trato.',
            'Funcionó perfectamente para mi proyecto. Recomiendo al propietario.',
            'Muy buena experiencia, herramienta de calidad y propietario confiable.',
            'Excelente estado de la herramienta, entrega y recogida puntuales.',
            'Herramienta profesional, me ayudó mucho en mi trabajo. Gracias!',
            'Muy satisfecho con el préstamo, herramienta como nueva.',
            'Propietario muy responsable y herramienta en excelentes condiciones.',
        ]
        
        comentarios_regulares = [
            'La herramienta funcionó bien, aunque podría estar en mejor estado.',
            'Cumplió con el trabajo, pero necesita un poco de mantenimiento.',
            'Herramienta funcional, trato correcto del propietario.',
            'Bien en general, algunas partes muestran desgaste normal.',
        ]
        
        comentarios_prestatario = [
            'Excelente prestatario, devolvió la herramienta en perfecto estado y a tiempo.',
            'Muy responsable, devolvió la herramienta limpia y en el tiempo acordado.',
            'Prestatario confiable, recomiendo prestarle herramientas sin problema.',
            'Buen prestatario, cuidó bien la herramienta. Comunicación fluida.',
            'Persona muy responsable, devolvió todo en orden.',
            'Excelente trato, devolvió la herramienta mejor de como la entregué.',
        ]
        
        for prestamo in prestamos_finalizados:
            try:
                with transaction.atomic():
                    # 90% de probabilidad de que el prestatario califique al propietario
                    if random.random() < 0.9:
                        puntaje = random.choices([3, 4, 5], weights=[10, 30, 60])[0]  # Más probabilidad de buenas calificaciones
                        
                        if puntaje >= 4:
                            comentario = random.choice(comentarios_positivos)
                        else:
                            comentario = random.choice(comentarios_regulares)
                        
                        calificacion1, created1 = Calificacion.objects.get_or_create(
                            prestamo=prestamo,
                            califica_usuario=prestamo.prestatario,
                            calificado_usuario=prestamo.herramienta.propietario,
                            defaults={
                                'puntaje': puntaje,
                                'comentario': comentario
                            }
                        )
                        if created1:
                            self.stdout.write(f"✅ Calificación creada: {prestamo.prestatario.username} -> {prestamo.herramienta.propietario.username} ({puntaje}⭐)")
                    
                    # 70% de probabilidad de que el propietario califique al prestatario
                    if random.random() < 0.7:
                        puntaje = random.choices([3, 4, 5], weights=[5, 25, 70])[0]  # Aún más probabilidad de buenas calificaciones
                        comentario = random.choice(comentarios_prestatario)
                        
                        calificacion2, created2 = Calificacion.objects.get_or_create(
                            prestamo=prestamo,
                            califica_usuario=prestamo.herramienta.propietario,
                            calificado_usuario=prestamo.prestatario,
                            defaults={
                                'puntaje': puntaje,
                                'comentario': comentario
                            }
                        )
                        if created2:
                            self.stdout.write(f"✅ Calificación creada: {prestamo.herramienta.propietario.username} -> {prestamo.prestatario.username} ({puntaje}⭐)")
                            
            except Exception as e:
                self.stdout.write(f"❌ Error al crear calificación: {e}")

    def mostrar_resumen(self):
        """Muestra un resumen de los datos creados"""
        self.stdout.write('\n📊 RESUMEN DE DATOS CREADOS:')
        self.stdout.write(f"👥 Usuarios: {Usuario.objects.count()}")
        self.stdout.write(f"🔧 Herramientas: {Herramienta.objects.count()}")
        self.stdout.write(f"📋 Préstamos: {Prestamo.objects.count()}")
        self.stdout.write(f"⭐ Calificaciones: {Calificacion.objects.count()}")
        
        self.stdout.write('\n📈 ESTADOS DE PRÉSTAMOS:')
        for estado, nombre in Prestamo.ESTADO_CHOICES:
            count = Prestamo.objects.filter(estado=estado).count()
            self.stdout.write(f"  {nombre}: {count}")
        
        self.stdout.write('\n🔑 CREDENCIALES DE ACCESO:')
        self.stdout.write('  Admin: usuario=admin, contraseña=admin123')
        self.stdout.write('  Vecinos: usuario=carlos_martinez, contraseña=123456')
        self.stdout.write('           usuario=ana_rodriguez, contraseña=123456')
        self.stdout.write('           usuario=miguel_lopez, contraseña=123456')
        self.stdout.write('           (y así sucesivamente para todos los vecinos)')
        
        self.stdout.write('\n🌐 ACCESO AL SISTEMA:')
        self.stdout.write('  Sistema: http://localhost:8000')
        self.stdout.write('  Admin Django: http://localhost:8000/admin')
        
        self.stdout.write('\n✨ ¡El sistema está listo para probar todas las funcionalidades!')
        self.stdout.write('\n📝 USUARIOS DISPONIBLES:')
        usuarios = Usuario.objects.filter(is_superuser=False)
        for usuario in usuarios:
            prestamos_count = Prestamo.objects.filter(prestatario=usuario).count()
            herramientas_count = Herramienta.objects.filter(propietario=usuario).count()
            self.stdout.write(f"  {usuario.username}: {herramientas_count} herramientas, {prestamos_count} préstamos")
