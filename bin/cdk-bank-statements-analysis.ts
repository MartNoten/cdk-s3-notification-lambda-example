#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { CdkBankStatementsAnalysisStack } from '../lib/cdk-bank-statements-analysis-stack';

const app = new cdk.App();
new CdkBankStatementsAnalysisStack(app, 'CdkBankStatementsAnalysisStack');
