# Continuous Autonomy Assurance

Green lanes are conditional permissions, not permanent permissions.

The assurance loop is:

```text
green-lane passport
-> registered assumptions
-> internal/external signals
-> assumption-watch record
-> autonomy reclassification record
-> human restoration packet, if green should be restored
```

Agents may downgrade green authority to yellow or red when assumptions become uncertain or false.

Agents may not:

- create new non-preapproved green authority;
- restore green authority after downgrade;
- approve yellow-to-green;
- bypass human review for red work.

Humans are required to create or restore non-preapproved green authority.

Assumption watch records must explain what changed, which assumptions were affected, and why the recommended reclassification is green-to-yellow, green-to-red, or unchanged.
