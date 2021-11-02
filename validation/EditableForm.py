from wtforms import Form, TextField, TextAreaField, SubmitField, validators, ValidationError, StringField, \
    PasswordField, SelectField
from wtforms.fields.html5 import EmailField
import email_validator
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import DateTimeField

# Clase de formulario personalizado, campo de texto, campo de contraseña, botón de envío
from wtforms.validators import DataRequired, EqualTo, Required
from wtforms.widgets.core import Select

from models.Destino import Destino


class EditableForm(Form):
    ########################################
    nombre = StringField('Nombre:', [validators.Regexp(r'^[\w]+$', message='Ingrese un nombre valido'),
                                     validators.Length(min=2, max=20)])
    apellidoP = StringField('Apellido Paterno:', [validators.Regexp(r'^[\w]+$', message='Ingrese un apellido valido'),
                                                  validators.Length(min=2, max=20,
                                                                    message='El apellido es demasiado corto')])
    apellidoM = StringField('Apellido Materno:', [validators.Regexp(r'^[\w]+$', message='Ingrese un apellido valido'),
                                                  validators.Length(min=2, max=20,
                                                                    message='El apellido es demasiado corto')])
    telefono = StringField('Telefono:', [validators.Regexp(r'^[0-9]+$', message='Porfavor ingrese solo numeros'),
                                         validators.Length(min=8, max=9, message='Escriba un numero valido')])
    fechaNacimiento = DateField('Fecha de Nacimiento:', default='',
                                validators=[validators.Required('Por favor Ingrese la fecha')], format='%Y-%m-%d')
    direccion = StringField('Direccion:', [validators.Required('Por favor Ingrese la direccion'),
                                           validators.Length(min=2, max=50, message='La direccion es muy corta')])

    correo = EmailField('Correo Electronico:', validators=[Required("Este campo es obligatorio"),
                                                           validators.Email(message='Ingrese un email valido')])
    """ contraseña = PasswordField('Contraseña:', [validators.Required("Este campo es obligatorio"),
                                               validators.Length(min=8, max=35,
                                                                 message='Ingrese una contraseña mas larga')]) """
    DNI = StringField('DNI:', [validators.Regexp(r'^[0-9]+$', message='Porfavor ingrese solo numeros'),
                                         validators.Length(min=8, max=8, message='Escriba un DNI valido')])
    # submit = SubmitField('enviar')

    departamentos = Destino().listDepartamentos()
    values = [("undefined", "Seleccione un departamento")]
    for row in departamentos:
        values.append((row.id_departamento, row.nombre))
    departamento = SelectField('Departamento:', choices=values, validators=[Required("Por favor seleccione un departamento")] )