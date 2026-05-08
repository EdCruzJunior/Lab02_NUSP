{% macro classificar_gravidade(col) %}
    case
        when {{ col }} >= 5 then 'ALTA'
        when {{ col }} >= 1 then 'MEDIA'
        else 'BAIXA'
    end
{% endmacro %}