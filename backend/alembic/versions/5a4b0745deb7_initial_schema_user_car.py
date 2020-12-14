"""Initial schema (User, Car)

Revision ID: 5a4b0745deb7
Revises:
Create Date: 2020-12-11 19:02:52.900219

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5a4b0745deb7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('model_name', sa.String(), nullable=False),
                    sa.Column('type', sa.Enum('CAR', 'TRUCK', 'SPORT', name='cartype'),
                              nullable=False),
                    sa.Column('fuel_type', sa.Enum('PETROL', 'DIESEL', 'HYBRID', 'EV',
                                                   name='fueltype'), nullable=False),
                    sa.Column('gearbox_type',
                              sa.Enum('AUTO', 'MANUAL', name='gearboxtype'),
                              nullable=False),
                    sa.Column('ac_type', sa.Enum('AUTO', 'MANUAL', name='actype'),
                              nullable=False),
                    sa.Column('number_of_passengers', sa.Integer(), nullable=False),
                    sa.Column('drive_type', sa.Enum('FRONT', 'REAR', 'ALL_WHEELS',
                                                    name='drivetype'), nullable=False),
                    sa.Column('average_consumption', sa.Float(), nullable=True),
                    sa.Column('number_of_airbags', sa.Integer(), nullable=False),
                    sa.Column('boot_capacity', sa.Float(), nullable=True),
                    sa.Column('price_per_day', sa.Numeric(precision=10, scale=2),
                              nullable=False),
                    sa.Column('deposit_amount', sa.Numeric(precision=10, scale=2),
                              nullable=True),
                    sa.Column('mileage_limit', sa.Float(), nullable=True),
                    sa.Column('image_base64', sa.String(), nullable=True),
                    sa.Column('loading_capacity', sa.Float(), nullable=True),
                    sa.Column('boot_width', sa.Float(), nullable=True),
                    sa.Column('boot_height', sa.Float(), nullable=True),
                    sa.Column('boot_length', sa.Float(), nullable=True),
                    sa.Column('horsepower', sa.Integer(), nullable=True),
                    sa.Column('zero_to_hundred_time', sa.Float(), nullable=True),
                    sa.Column('engine_capacity', sa.Float(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_car_ac_type'), 'car', ['ac_type'], unique=False)
    op.create_index(op.f('ix_car_drive_type'), 'car', ['drive_type'], unique=False)
    op.create_index(op.f('ix_car_fuel_type'), 'car', ['fuel_type'], unique=False)
    op.create_index(op.f('ix_car_gearbox_type'), 'car', ['gearbox_type'], unique=False)
    op.create_index(op.f('ix_car_horsepower'), 'car', ['horsepower'], unique=False)
    op.create_index(op.f('ix_car_id'), 'car', ['id'], unique=False)
    op.create_index(op.f('ix_car_loading_capacity'), 'car', ['loading_capacity'],
                    unique=False)
    op.create_index(op.f('ix_car_model_name'), 'car', ['model_name'],
                    unique=False)
    op.create_index(op.f('ix_car_price_per_day'), 'car', ['price_per_day'],
                    unique=False)
    op.create_index(op.f('ix_car_type'), 'car', ['type'], unique=False)
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('full_name', sa.String(), nullable=True),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('hashed_password', sa.String(), nullable=False),
                    sa.Column('is_admin', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_car_type'), table_name='car')
    op.drop_index(op.f('ix_car_price_per_day'), table_name='car')
    op.drop_index(op.f('ix_car_model_name'), table_name='car')
    op.drop_index(op.f('ix_car_loading_capacity'), table_name='car')
    op.drop_index(op.f('ix_car_id'), table_name='car')
    op.drop_index(op.f('ix_car_horsepower'), table_name='car')
    op.drop_index(op.f('ix_car_gearbox_type'), table_name='car')
    op.drop_index(op.f('ix_car_fuel_type'), table_name='car')
    op.drop_index(op.f('ix_car_drive_type'), table_name='car')
    op.drop_index(op.f('ix_car_ac_type'), table_name='car')
    op.drop_table('car')
    # ### end Alembic commands ###