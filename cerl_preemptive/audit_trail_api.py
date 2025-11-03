PORT), AuditHandler) as httpd:
        print(f"Audit Trail API running at http://localhost:{port}/")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()