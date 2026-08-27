# Dokumentacja wellmanifest/sch

Standard opisuje **dokumenty**, nie polecenia: adopter wczytuje profil i porównuje
wynik ze swoim rysunkiem. Dlatego `documentation.vocabularyKind` to `documents`,
a listy `commands`, `errorCodes` i `criticalCodes` są puste.

Kody bramki (`SCH_STYLE_REGRESSION`, `SCH_STYLE_NOT_RUN`) należą do przestrzeni
adoptera i używają podkreśleń, więc nie pasują do wzorca `findingCode`
z `wellmanifest.dsl/manifest/v1`. Mapowanie powstanie razem z przyjęciem
`wellmanifest/dsl`, żeby jedno zdarzenie nie miało dwóch nazw.
