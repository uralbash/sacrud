0.3.7 (2016-05-09)
------------------

- fix columns_by_group function

0.3.6 (2016-01-07)
------------------

- fix common.get_obj function

0.3.5 (2015-12-02)
------------------

- fix create/update with sqlalchemy.sql.null value

0.3.4 (2015-11-30)
------------------

- delete exttype module
- fix bug when list JSON gets corrupted #105 

0.3.3 (2015-10-09)
------------------

- Fix slug exttype
- Now work with Postgres JSON and JSONB columns

0.3.2 (2015-07-10)
------------------

- Add support JSON format for input values #104

0.3.1 (2015-06-30)
------------------

- return query object instead list, when do ``read`` action with multiple primary keys.

0.3.0 (2015-06-29)
------------------

- fix ``Boolean`` field with default value ITCase/pyramid_sacrud#94

0.2.9 (2015-06-12)
------------------

- fix ``sacrud_detail_col`` table attribute

0.2.8 (2015-06-11)
------------------

- Added ``sacrud.common.ClassProperty``

0.2.7 (2015-06-04)
------------------

- Added ``update`` option for create action.

0.2.6 (2015-05-30)
------------------

- Prohiit add an existing object

0.2.5 (2015-04-05)
------------------

- Fix SQLAlchemy version in requirements

0.2.4 (2015-03-30)
------------------

- Added class ``CRUDSession`` for ``class_`` attribute in sessionmaker #102

0.2.3 (2015-03-15)
------------------

- Added attribute ``commit`` to ``create`` and ``update`` function.
- Write docs for m2o and m2o data.

0.2.2 (2015-03-09)
------------------

- New API!!!
- Added wrapper ``crud_sessionmaker`` for SQLAlchemy session.
- More tests.

0.2.1 (2015-03-08)
------------------

- Added support ``Date`` and ``DateTime`` object in request.
- Restructured preprocessing.

