import sys
import os
from sqlalchemy import func, select, column

# Ensure the local version of the code is used for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# Import the Flight dialect
from sqlalchemy_dremio.flight import DremioDialect_flight


def test_dremio_date_translations():
    dialect = DremioDialect_flight()

    # Test DATEDIFF -> DATE_SUB
    stmt_datediff = select(func.datediff(func.current_date(), 30))

    compiled_datediff = str(stmt_datediff.compile(
        dialect=dialect,
        compile_kwargs={"literal_binds": True}
    ))

    print(f"Compiled SQL: {compiled_datediff}")

    # Assertions
    assert "DATE_SUB" in compiled_datediff
    assert "DATEDIFF" not in compiled_datediff


if __name__ == "__main__":
    try:
        test_dremio_date_translations()
        print("✅ Success: DATEDIFF correctly translated to DATE_SUB.")
    except AssertionError as e:
        print(f"❌ Failure: Translation was incorrect.")
        raise e
