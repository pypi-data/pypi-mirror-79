{% macro oracle_basic_load_csv_rows(model, batch_size, agate_table) %}

    {% set cols_sql = get_seed_column_quoted_csv(model, agate_table.column_names) %}
    {% set bindings = [] %}

    {% set statements = [] %}

    {% for chunk in agate_table.rows | batch(batch_size) %}
        {% set bindings = [] %}

        {% for row in chunk %}
            {% do bindings.extend(row) %}
        {% endfor %}

        {% set sql %}
            insert all
            {% for row in chunk -%}
              into {{ this.render() }} ({{ cols_sql }}) values(
                {%- for column in agate_table.column_names -%}
                    :p{{ loop.index }} 
                    {%- if not loop.last%},{%- endif %}
                {%- endfor %})
            {% endfor %}
            select * from dual
        {% endset %}

        {% do adapter.add_query(sql, bindings=bindings, abridge_sql_log=True) %}

        {% if loop.index0 == 0 %}
            {% do statements.append(sql) %}
        {% endif %}
    {% endfor %}

    {# Return SQL so we can render it out into the compiled files #}
    {{ return(statements[0]) }}
{% endmacro %}

{% macro oracle__load_csv_rows(model, agate_table) %}
  {{ return(oracle_basic_load_csv_rows(model, 100, agate_table) )}}
{% endmacro %}

