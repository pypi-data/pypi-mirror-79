from django.db import migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunSQL(
            sql='''
                CREATE AGGREGATE PRODUCT(numeric)(sfunc = numeric_mul, stype = numeric);
                CREATE AGGREGATE PRODUCT(integer)(sfunc = int4mul, stype = integer);
                CREATE AGGREGATE PRODUCT(bigint)(sfunc = int8mul, stype = bigint);
                CREATE AGGREGATE PRODUCT(real)(sfunc = float4mul, stype = real);
                CREATE AGGREGATE PRODUCT(double precision)(sfunc = float8mul, stype = double precision);
                ''',
            reverse_sql='''
                DROP AGGREGATE PRODUCT(numeric);
                DROP AGGREGATE PRODUCT(integer);
                DROP AGGREGATE PRODUCT(bigint);
                DROP AGGREGATE PRODUCT(real);
                DROP AGGREGATE PRODUCT(double precision);
                ''')
    ]
