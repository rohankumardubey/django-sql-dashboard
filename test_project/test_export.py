def test_export_csv(admin_client, dashboard_db):
    response = admin_client.post(
        "/dashboard/",
        {
            "sql": "SELECT 'hello' as label, * FROM generate_series(0, 10000)",
            "export_csv_0": "1",
        },
    )
    body = b"".join(response.streaming_content)
    assert body.startswith(
        b"label,generate_series\r\nhello,0\r\nhello,1\r\nhello,2\r\n"
    )
    assert body.endswith(b"hello,9998\r\nhello,9999\r\nhello,10000\r\n")
    assert response["Content-Type"] == "text/csv"
    content_disposition = response["Content-Disposition"]
    assert content_disposition.startswith(
        'attachment; filename="select--hello--as-label'
    )
    assert content_disposition.endswith('.csv"')


def test_export_tsv(admin_client, dashboard_db):
    response = admin_client.post(
        "/dashboard/",
        {
            "sql": "SELECT 'hello' as label, * FROM generate_series(0, 10000)",
            "export_tsv_0": "1",
        },
    )
    body = b"".join(response.streaming_content)
    assert body.startswith(
        b"label\tgenerate_series\r\nhello\t0\r\nhello\t1\r\nhello\t2\r\n"
    )
    assert body.endswith(b"hello\t9998\r\nhello\t9999\r\nhello\t10000\r\n")
    assert response["Content-Type"] == "text/tab-separated-values"
    content_disposition = response["Content-Disposition"]
    assert content_disposition.startswith(
        'attachment; filename="select--hello--as-label'
    )
    assert content_disposition.endswith('.tsv"')