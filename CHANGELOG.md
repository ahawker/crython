# Change Log

## [Unreleased](https://github.com/ahawker/crython/tree/HEAD)

[Full Changelog](https://github.com/ahawker/crython/compare/v0.0.8...HEAD)

**Closed issues:**

- pyup.io:  Initial Update [\#43](https://github.com/ahawker/crython/issues/43)

**Merged pull requests:**

- Add Python code security linting with bandit. [\#45](https://github.com/ahawker/crython/pull/45) ([ahawker](https://github.com/ahawker))
- Add package dependency security scan using 'safety' package. [\#44](https://github.com/ahawker/crython/pull/44) ([ahawker](https://github.com/ahawker))
- Add build requirements to fix 3.4.6 setuptools regression. [\#42](https://github.com/ahawker/crython/pull/42) ([ahawker](https://github.com/ahawker))
- Remove coveralls usage. [\#41](https://github.com/ahawker/crython/pull/41) ([ahawker](https://github.com/ahawker))
- Pin all requirements to latest versions. [\#40](https://github.com/ahawker/crython/pull/40) ([ahawker](https://github.com/ahawker))
- Update setup.py to use restructured text documentation. [\#39](https://github.com/ahawker/crython/pull/39) ([ahawker](https://github.com/ahawker))
- Address pylint related issues. [\#38](https://github.com/ahawker/crython/pull/38) ([ahawker](https://github.com/ahawker))

## [v0.0.8](https://github.com/ahawker/crython/tree/v0.0.8) (2017-08-24)
[Full Changelog](https://github.com/ahawker/crython/compare/v0.0.7...v0.0.8)

**Closed issues:**

- Expression "@reboot" does not work [\#34](https://github.com/ahawker/crython/issues/34)

**Merged pull requests:**

- Fix equality bug on reboot expressions. [\#36](https://github.com/ahawker/crython/pull/36) ([ahawker](https://github.com/ahawker))

## [v0.0.7](https://github.com/ahawker/crython/tree/v0.0.7) (2017-05-28)
[Full Changelog](https://github.com/ahawker/crython/compare/v0.0.6...v0.0.7)

**Fixed bugs:**

- Weekday should support 0-7 range; 7 being Sunday. [\#15](https://github.com/ahawker/crython/issues/15)
- Range "10-26/8" matches "14". [\#13](https://github.com/ahawker/crython/issues/13)

**Closed issues:**

- Does not work in python3.5 [\#31](https://github.com/ahawker/crython/issues/31)

**Merged pull requests:**

- Fix inconsistency between Cron & struct\_time for what day is zero. [\#33](https://github.com/ahawker/crython/pull/33) ([ahawker](https://github.com/ahawker))
- Fix equation for computing value inclusion in range with step. [\#32](https://github.com/ahawker/crython/pull/32) ([ahawker](https://github.com/ahawker))

## [v0.0.6](https://github.com/ahawker/crython/tree/v0.0.6) (2017-05-25)
[Full Changelog](https://github.com/ahawker/crython/compare/v0.0.5...v0.0.6)

**Fixed bugs:**

- \*/int syntax doesn't appear to work [\#29](https://github.com/ahawker/crython/issues/29)

## [v0.0.5](https://github.com/ahawker/crython/tree/v0.0.5) (2017-04-07)
[Full Changelog](https://github.com/ahawker/crython/compare/v0.0.4...v0.0.5)

**Merged pull requests:**

- Fix int/str type comparisons for py27/py3. [\#30](https://github.com/ahawker/crython/pull/30) ([ahawker](https://github.com/ahawker))
- Update README.md [\#28](https://github.com/ahawker/crython/pull/28) ([angrybabayev](https://github.com/angrybabayev))

## [v0.0.4](https://github.com/ahawker/crython/tree/v0.0.4) (2017-02-07)
[Full Changelog](https://github.com/ahawker/crython/compare/v0.0.3...v0.0.4)

**Fixed bugs:**

- cron jobs run every second\(bug\) [\#24](https://github.com/ahawker/crython/issues/24)
- get an Exception when you try to new a tab using 'logger' keyword [\#23](https://github.com/ahawker/crython/issues/23)
- Update the pypy version [\#8](https://github.com/ahawker/crython/issues/8)

**Merged pull requests:**

- Fix fields\_lazy\_eval match bug. [\#26](https://github.com/ahawker/crython/pull/26) ([ahawker](https://github.com/ahawker))
- Don't pass args/kwargs to thread init. [\#25](https://github.com/ahawker/crython/pull/25) ([ahawker](https://github.com/ahawker))
- Add initial Sphinx documentation support. [\#22](https://github.com/ahawker/crython/pull/22) ([ahawker](https://github.com/ahawker))
- Add "codeclimate" make target for running local analysis. [\#21](https://github.com/ahawker/crython/pull/21) ([ahawker](https://github.com/ahawker))
- Add pep8 support to codeclimate integ. [\#20](https://github.com/ahawker/crython/pull/20) ([ahawker](https://github.com/ahawker))
- Add a Gitter chat badge to README.md [\#19](https://github.com/ahawker/crython/pull/19) ([gitter-badger](https://github.com/gitter-badger))

## [v0.0.3](https://github.com/ahawker/crython/tree/v0.0.3) (2017-01-22)
[Full Changelog](https://github.com/ahawker/crython/compare/v0.0.2...v0.0.3)

## [v0.0.2](https://github.com/ahawker/crython/tree/v0.0.2) (2017-01-15)
**Implemented enhancements:**

- Support Python 3.X [\#12](https://github.com/ahawker/crython/issues/12)

**Merged pull requests:**

- README: fix how to start, now calls run\(\) [\#7](https://github.com/ahawker/crython/pull/7) ([aisipos](https://github.com/aisipos))
- Backward compatibility for python 2.6 [\#3](https://github.com/ahawker/crython/pull/3) ([harryliang](https://github.com/harryliang))
- Updated test\_field to fix failing tests. [\#2](https://github.com/ahawker/crython/pull/2) ([ahawker](https://github.com/ahawker))
- Add missing '@' to README.md [\#1](https://github.com/ahawker/crython/pull/1) ([jtratner](https://github.com/jtratner))



\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*